import logging
from cassandra import ReadTimeout, WriteTimeout
from cassandra.cqlengine.query import DoesNotExist

from dal.base import BaseDAL
from models.following_users import FollowingUserMap


log = logging.getLogger(__name__)


class FollowingConnectionDAL(BaseDAL):

    def add(self, email, payload):
        try:
            user_map = FollowingUserMap(
                email=email,
                following_user_email=payload["following_user_email"])
            user_map.save()
            log.info("added the following_user {} to user: {}".format(
                payload["following_user_email"],
                email))
            return True
        except WriteTimeout as e:
            raise e

    def get(self, email):
        try:
            query = FollowingUserMap.objects.filter(email=email)
            users = query.all()
            log.info("resultset :{}".format(users))
            return self.format_list(users)
        except DoesNotExist:
            log.exception("following users does not exists for email:{}".format(email))
            return []
        except ReadTimeout as e:
            log.exception(
                "Failed to get following users:{} for email:{}".format(e, email))
            raise e
        except Exception as e:
            log.exception("Failed to get following users:{}".format(e, email))
            raise e

    def delete(self, email, following_user_email):
        try:
            query = FollowingUserMap.objects.filter(
                email=email, following_user_email=following_user_email)
            query.delete()
            log.info("deleted following users for :{}".format(email))
            return True
        except DoesNotExist:
            log.exception(
                "following users does not exists for email:{}".format(email))
            return True
        except WriteTimeout as e:
            log.exception(
                "Failed to delete following users for email:{} {}".format(
                    email, e))
            raise e
        except Exception as e:
            log.exception("Failed to delete following users for email:{} {}".format(
                email, e))
            raise e
