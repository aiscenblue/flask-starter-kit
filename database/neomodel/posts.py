from neomodel import (StructuredNode, UniqueIdProperty, RelationshipTo, StringProperty, DateTimeProperty)
from database.neo4j.neomodel.edges.timestamp import EdgeRelationship
from database.neo4j.neomodel.users import Users


class Posts(StructuredNode):
    uid = UniqueIdProperty()
    content = StringProperty(required=True)
    author = RelationshipTo(Users, "AUTHOR", model=EdgeRelationship)
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
        if "user_id" in kwargs:
            author = Users().find_by_id(uid=kwargs['user_id'])
            if author:
                saved_post = super().save()
                """ save post relationship after saving the post node """
                self.author.connect(author)
                return saved_post
            else:
                raise LookupError("Invalid author.")
        else:
            raise KeyError("user ID is required.")
