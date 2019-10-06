import json
import logging
from cassandra.cqlengine import connection as cqlconnection

from conf.settings import Config
from common.constants import CassandraKeySpaces
from common.utils import Singleton

log = logging.getLogger(__name__)


@Singleton
class CassandraDB:
    '''
    Default load distribution is Round Robin
    '''
    connected = False
    prepared_stmt = dict()

    def connect(self):
        try:

            if cqlconnection.cluster is not None:
                log.info("Shutdown cassandra cluster connection")
                cqlconnection.cluster.shutdown()

            if cqlconnection.session is not None:
                log.info("Shutdown cassandra session")
                cqlconnection.session.shutdown()

            cqlconnection.setup(Config.cassandra_hosts,
                                CassandraKeySpaces.USERDB,
                                retry_connect=True)
        except:
            log.exception("Cassandra Cluster is not reachable")
            self.connected = False
            raise
        else:
            self.connected = True
            return cqlconnection.session

    def prepared_stmts(self):
        return self.prepared_stmt


class BaseDAL(object):
    def __init__(self):
        self.db_object = CassandraDB()
        self.session = self.db_object.connect()

    def format(self, db_object):
        row = dict()
        for column, value in db_object.items():
            if isinstance(value, str):
                if value.isdigit():
                    row[column] = value
                else:
                    try:
                        row[column] = json.loads(value)
                    except ValueError:
                        row[column] = value
            else:
                row[column] = value
        return row

    def format_list(self, db_obj):
        return [self.format(obj) for obj in db_obj]
