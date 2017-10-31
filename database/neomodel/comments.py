from neomodel import (StructuredNode, UniqueIdProperty, RelationshipTo, StringProperty, DateTimeProperty)
from database.neo4j.neomodel.edges.timestamp import EdgeRelationship
from database.neo4j.neomodel.users import Users
from database.neo4j.neomodel.posts import Posts


class Comments(StructuredNode):
    uid = UniqueIdProperty()
    content = StringProperty(required=True)
    author = RelationshipTo(Users, "AUTHOR", model=EdgeRelationship)
    post = RelationshipTo(Posts, "COMMENTED_ON", model=EdgeRelationship)
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    deleted_at = DateTimeProperty(required=False, default=None)

    def find(self, page=0, per_page=15, **kwargs):
        skip = 0 if page <= 1 else page - 1
        limit = skip + per_page
        order_by = 'created_at'

        if "order_by" in kwargs and kwargs['order_by']:
            order_by = kwargs['order_by']
        if "uid" in kwargs and kwargs['uid']:
            return self.find_by_id(uid=kwargs['uid'])
        else:
            return self.nodes.order_by(order_by).filter(deleted_at__isnull=True)[skip:limit]

    def find_by_id(self, uid):
        return self.nodes.get(uid=uid, deleted_at__isnull=True)

    def save(self, **kwargs):
        if "user_id" in kwargs and "post_id" in kwargs:
            author = Users().find_by_id(uid=kwargs['user_id'])
            post = Posts().find_by_id(uid=kwargs['post_id'])

            if author and post and post.author.get().__dict__["uid"] == kwargs['user_id']:
                saved_comment = super().save()
                self.author.connect(author)
                self.post.connect(post)
                return saved_comment
            else:
                raise LookupError("Invalid author or post.")
        else:
            raise KeyError("Missing required parameters")
