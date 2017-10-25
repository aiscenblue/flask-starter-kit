from flask import Blueprint, make_response

""" blueprint module for url handler """
__method__ = Blueprint(__name__, __name__)
app = __method__


@app.route("/", methods=['GET'])
def index():
    return make_response("Welcome to flask starter kit!", 200)
