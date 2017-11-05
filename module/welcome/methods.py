from flask import make_response, request, jsonify
from database.neomodel.users import Users
import jwt
import weakref
import string
import random


class Methods:

    @staticmethod
    def index():
        return make_response("Welcome module", 200)

    @staticmethod
    def create():
        return make_response("Welcome POST method", 200)

    @staticmethod
    def update():
        return make_response("Welcome PUT method", 200)

    @staticmethod
    def destroy():
        return make_response("Welcome DELETE method", 200)

