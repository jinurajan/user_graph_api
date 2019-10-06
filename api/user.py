# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask import request

from common.errors import BadRequestError
from common.validators import UserCreationValidator, UserUpdationValidator
from services.user import UserService


class UserListHandler(Resource):
    def get(self):
        return UserService.get_all()

    def post(self):
        payload = request.json
        valid, errors = UserCreationValidator().validate(payload)
        if not valid:
            raise BadRequestError("Invalid Request", errors)
        return UserService.add(payload)


class UserHandler(Resource):
    def get(self, email):
        return UserService.get(email)

    def put(self, email):
        payload = request.json
        valid, errors = UserUpdationValidator().validate(payload)
        if not valid:
            raise BadRequestError("Invalid Request", errors)
        return UserService.update(email, payload)

    def delete(self, email):
        return UserService.delete(email)
