# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask import request

from common.errors import BadRequestError
from common.validators import UserFollowCreationValidator
from services.following_users import UserFollowService


class FollowUserListHandler(Resource):
    def get(self, email):
        return UserFollowService.get(email)

    def put(self, email):
        payload = request.json
        valid, errors = UserFollowCreationValidator().validate(payload)
        if not valid:
            raise BadRequestError("Invalid Request", errors)
        return UserFollowService.add(email, payload)


class FollowUserHandler(Resource):

    def delete(self, email, following_user_email):
        return UserFollowService.delete(email, following_user_email)
