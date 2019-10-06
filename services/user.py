
from common.errors import NotFoundError, ConflictError
from dal.user import UserDAL
from dal.following_users import FollowingConnectionDAL


class UserService(object):

    @classmethod
    def add(self, payload):
        try:
            user_dal = UserDAL()
            if user_dal.get(payload["email"]):
                raise ConflictError(
                    "User:{} Already Exists".format(
                        payload["email"]))
            user_dal.add(payload)
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
            following_users = []
            for user in conn_dal.get(email):
                following_users.append({
                    "following_user_email": user["following_user_email"],
                    "created_at": user["created_at"]
                })

            result["following_users"] = following_users
            return result
        except Exception as e:
            raise e

    @classmethod
    def update(self, email, payload):
        try:
            user_dal = UserDAL()
            user = user_dal.get(email)
            if not user:
                raise NotFoundError("User:{} Not Found".format(email))
            user_dal.update(email, payload)
        except Exception as e:
            raise e

    @classmethod
    def delete(self, email):
        try:
            user_dal = UserDAL()
            user = user_dal.get(email)
            if not user:
                raise NotFoundError("User:{} Not Found".format(email))
            user_dal.delete(email)
        except Exception as e:
            raise e

    @classmethod
    def get_all(self):
        try:
            user_dal = UserDAL()
            return user_dal.list()
        except Exception as e:
            raise e
