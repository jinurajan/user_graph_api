import time
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from common.constants import CassandraKeySpaces


class User(Model):
    __keyspace__ = CassandraKeySpaces.USERDB
    email = columns.Text(primary_key=True, partition_key=True)
    phone = columns.Text(required=True)
    name = columns.Text(required=True)
    created_at = columns.Integer(default=int(time.time()))
    updated_at = columns.Integer(default=int(time.time()))
