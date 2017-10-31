from flask import make_response, request, jsonify
from database.neomodel.locations import Locations


class Methods:

    @staticmethod
    def index():
        req = request.args
        page = int(req.get('page')) if req.get('page') else 0
        per_page = int(req.get('per_page')) if req.get('per_page') else 15
        uid = req.get('uid') or None
        order_by = req.get('order_by') or None
        return make_response(jsonify(
            [location.__dict__ for location in Locations().find(page, per_page, uid=uid, order_by=order_by)]), 200)

    @staticmethod
    def create():
        pass

    @staticmethod
    def update():
        return make_response("Welcome PUT method", 200)

    @staticmethod
    def destroy():
        return make_response("Welcome DELETE method", 200)
