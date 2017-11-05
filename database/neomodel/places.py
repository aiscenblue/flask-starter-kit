from database.neomodel.locations import Locations
from neomodel import (StructuredNode, StringProperty, DateTimeProperty, UniqueIdProperty, RelationshipTo, JSONProperty, ArrayProperty, IntegerProperty)
from database.neomodel.edges.timestamp import EdgeRelationship


class Places(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    reference = StringProperty(required=True)
    types = ArrayProperty(default=None)
    formatted_address = StringProperty(required=True)
    opening_hours = JSONProperty(required=False)
    rating = IntegerProperty(required=False)
    photos = JSONProperty(required=False)
    place_id = StringProperty(required=True)
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    deleted_at = DateTimeProperty(default_now=False)
    locations = RelationshipTo(Locations, "LOCATED_AT", model=EdgeRelationship)

    def find(self, page=0, per_page=15, **kwargs):
        skip = 0 if page <= 1 else page - 1
        limit = skip + per_page
        order_by = 'created_at'

        if "order_by" in kwargs and kwargs['order_by']:
            order_by = kwargs['order_by']
        if "uid" in kwargs and kwargs['uid']:
            return self.find_by_id(uid=kwargs['uid'])
        else:
            return self.nodes.has(locations=True).order_by(order_by).filter(deleted_at__isnull=True)[skip:limit]

    def find_by_id(self, uid):
        return self.nodes.has(locations=True).get(uid=uid, deleted_at__isnull=True)

    def save(self, **kwargs):
        if "location_id" in kwargs:
            location = Locations().find_by_id(uid=kwargs['location_id'])
            if location:
                saved_location = super(Places, self).save()
                """ save location relationship after saving the place node """
                self.locations.connect(location)
                return saved_location
            else:
                raise LookupError("Location ID not found.")
        else:
            raise LookupError("Location not found.")
