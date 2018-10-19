from flask import make_response


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
