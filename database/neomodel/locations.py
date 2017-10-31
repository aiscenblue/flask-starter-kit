from neomodel import (StructuredNode, UniqueIdProperty, FloatProperty, StringProperty, JSONProperty, DateTimeProperty)


class Locations(StructuredNode):
    uid = UniqueIdProperty()
    country = StringProperty(required=True)
    latitude = FloatProperty(required=True)
    longitude = FloatProperty(required=True)
    viewport = JSONProperty(required=False)
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
