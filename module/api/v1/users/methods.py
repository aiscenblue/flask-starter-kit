from flask import make_response, request, jsonify
from database.neomodel.users import Users
import jwt
import random
import string
import weakref


class Methods:

    @staticmethod
    def index():
        try:
            req = request.args
            page = int(req.get('page')) if req.get('page') else 0
            per_page = int(req.get('per_page')) if req.get('per_page') else 15
            uid = req.get('uid') or None
            order_by = req.get('order_by') or None
            users = Users().find(page, per_page, uid=uid, order_by=order_by)

            return make_response(jsonify([user.__dict__ for user in users]), 200)

        except (KeyError, LookupError, ValueError) as error:
            return make_response(jsonify(str(error)), 500)

    @staticmethod
    def create():
        try:
            req = request.form
            user_data = Users(
                firstname=req.get("first_name"),
                lastname=req.get("last_name"),
                email=req.get("email"),
                password=req.get("password")
            ).save()

            del user_data.__dict__["password"]
            user_data.__dict__["created_at"] = str(user_data.__dict__["created_at"])
            user_data.__dict__["updated_at"] = str(user_data.__dict__["updated_at"])
            secret_key = ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
            encoded_jwt = jwt.encode(user_data.__dict__, secret_key, algorithm='HS256')

            return make_response(jsonify({
                "data": user_data.__dict__,
                "secret_key": secret_key,
                "access_token": encoded_jwt,
                "message": "Successfully created!"
            }), 200)

        except (KeyError, LookupError, ValueError) as error:
            return make_response(jsonify(str(error)), 500)
        except TypeError as e:
            print(e)
            return make_response(jsonify("Missing parameter."), 500)

    @staticmethod
    def update():
        return make_response("Welcome PUT method", 200)

    @staticmethod
    def destroy():
        return make_response("Welcome DELETE method", 200)

    @staticmethod
    def authenticate():
        try:
            req = request.form
            users = Users(email=req.get("email"), password=req.get("password")).authenticate()
            user_ref = weakref.ref(users)

            del user_ref().__dict__["password"]
            secret_key = ''.join(
                random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
            encoded_jwt = jwt.encode(user_ref().__dict__, secret_key, algorithm='HS256')

            return make_response(
                jsonify({"data": user_ref().__dict__, "secret_key": secret_key, "access_token": encoded_jwt}), 200)
        except (LookupError, ValueError) as error:
            return make_response(jsonify(str(error)), 500)
