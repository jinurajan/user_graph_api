import time
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from common.constants import CassandraKeySpaces


class FollowingUserMap(Model):
    __keyspace__ = CassandraKeySpaces.USERDB
    email = columns.Text(primary_key=True, partition_key=True)
    following_user_email = columns.Text(primary_key=True, required=True)
    created_at = columns.Integer(default=int(time.time()))
