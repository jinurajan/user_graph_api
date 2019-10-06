import logging
import time
from cassandra import ReadTimeout, WriteTimeout
from cassandra.cqlengine.query import DoesNotExist
from dal.base import BaseDAL
from models.user import User
from models.following_users import FollowingUserMap

log = logging.getLogger(__name__)


class UserDAL(BaseDAL):

    def add(self, payload):
        try:
            user = User(
                email=payload["email"],
                name=payload["name"],
                phone=payload["phone"])
            user.save()
            log.info("added the user: {}"
                     .format(payload["email"]))
            return self.format(payload)
        except WriteTimeout as e:
            log.exception(
                "Unable to Create user with email:{} error:{}".format(
                    payload["email"], e))
            raise e

    def update(self, email, payload):
        try:
            user = User(
                email=email,
                name=payload["name"],
                phone=payload["phone"],
                updated_at=int(time.time()))
            user.save()
            log.info("updated the user: {}"
                     .format(email))
            return self.format(payload)
        except WriteTimeout as e:
            log.exception(
                "Unable to Update user with email:{} error:{}".format(
                    email, e))
            raise e

    def get(self, email):
        try:
            query = User.objects.filter(email=email)
            user = query.first()
            if user:
                log.info("resultset :{}".format(user))
                return self.format(user)
            else:
                return None
        except ReadTimeout as e:
            log.exception(
                "Failed to get user:{} for email:{}".format(e, email))
            raise e
        except Exception as e:
            log.exception("Failed to get user:{}".format(e, email))
            raise e

    def delete(self, email):
        try:
            """
            delete the connected users of email before deleting the user.
            This should be done asynchronously since there can be
            many users associated
            """
            query = FollowingUserMap.objects.filter(email=email)
            query.delete()
            query = User.objects.filter(email=email)
            query.delete()
            log.info("deleted the user with email :{}"
                     .format(email))
            return True
        except Exception as e:
            log.exception("Failed to delete the user:{} {}".format(email, e))
            raise e

    def list(self):
        try:
            query = User.objects
            users = query.all()
            log.info("resultset :{}".format(users))
            return self.format_list(users)
        except DoesNotExist:
            log.exception("users does not exists")
            return []
        except ReadTimeout as e:
            log.exception(
                "Failed to get users")
            raise e
        except Exception as e:
            log.exception("Failed to get users")
            raise e
