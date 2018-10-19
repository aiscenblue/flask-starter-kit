from flask import make_response


def index():
    return make_response("Home module", 200)
