from neomodel import (StructuredRel, DateTimeProperty)


class EdgeRelationship(StructuredRel):
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    deleted_at = DateTimeProperty(required=False, default=None)
