from flask import make_response, request, jsonify
from database.neomodel.posts import Posts
from database.neomodel.media import Media


class Methods:

    @staticmethod
    def index():
        req = request.args
        page = int(req.get('page')) if req.get('page') else 0
        per_page = int(req.get('per_page')) if req.get('per_page') else 15
        uid = req.get('uid') or None
        order_by = req.get('order_by') or None

        posts = Posts().find(page, per_page, uid=uid, order_by=order_by)
        data = []

        for post in posts:
            __post = post.__dict__
            __post['author'] = post.author.get().__dict__
            data.append(__post)

        return make_response(jsonify(data), 200)

    @staticmethod
    def create():
        try:
            req = request.form
            # check if the post request has the file part
            if request.files:
                print(Media().upload(files=request.files))
            post_data = Posts(
                content=req.get("content"),
            ).save(user_id=req.get("user_id"))
            data = post_data.__dict__
            data['author'] = post_data.author.get().__dict__

            return make_response(jsonify({
                "data": data,
                "message": "Success!"
            }), 301)
        except (KeyError, LookupError) as error:
            return make_response(jsonify(str(error)), 500)

    @staticmethod
    def update():
        return make_response("Welcome PUT method", 200)

    @staticmethod
    def destroy():
        return make_response("Welcome DELETE method", 200)
