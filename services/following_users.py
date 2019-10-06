
from common.errors import NotFoundError, ConflictError
from dal.user import UserDAL
from dal.following_users import FollowingConnectionDAL
from models.following_users import FollowingUserMap


class UserFollowService(object):

    @classmethod
    def add(self, email, payload):
        try:
            user_dal = UserDAL()
            if not user_dal.get(email):
                raise NotFoundError(
                    "User:{} does not exists".format(
                        email))
            follow_dal = FollowingConnectionDAL()
            follow_dal.add(email, payload)
            # TODO: Background task to run dijkstra's algorithm to be done here
        except Exception as e:
            raise e

    @classmethod
    def get(self, email):
        try:
            user_dal = UserDAL()
            result = user_dal.get(email)
            if not result:
                raise NotFoundError("User:{} Not Found".format(email))
            conn_dal = FollowingConnectionDAL()
            following_users = [user["following_user_email"] for user in conn_dal.get(email)]
            return {"following_users": following_users}
        except Exception as e:
            raise e

    @classmethod
    def delete(self, email, follow_email):
        try:
            user_dal = UserDAL()
            user = user_dal.get(email)
            if not user:
                raise NotFoundError("User:{} Not Found".format(email))
            conn_dal = FollowingConnectionDAL()
            conn_dal.delete(email, follow_email)
            # TODO: Background task to run dijkstra's algorithm to be done here
        except Exception as e:
            raise e
