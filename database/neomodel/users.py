from neomodel import (StructuredNode, UniqueIdProperty, StringProperty, EmailProperty, DateTimeProperty, db)
from validators import email as email_validator
import bcrypt


class Users(StructuredNode):
    uid = UniqueIdProperty()
    first_name = StringProperty(required=True)
    middle_name = StringProperty(default=None)
    last_name = StringProperty(required=True)
    email = EmailProperty(unique_index=True, required=True)
    password = StringProperty(required=True)
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    deleted_at = DateTimeProperty(required=False, default=None)

    def __init__(self, *args, **kwargs):
        super(StructuredNode, self).__init__(*args, **kwargs)

    def _validate_email_format(self, email=None):
        __email = email or self.email
        if not email_validator(__email):
            raise KeyError("Email is invalid format.")
        else:
            return None

    def find_by_email(self, email=None):
        __email = email or self.email
        return self.nodes.order_by('created_at').filter(email=__email, deleted_at__isnull=True)

    def _hash_password(self):
        if hasattr(self, "password"):
            self.password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt()).decode()

    def authenticate(self):

        user = self.find_by_email()

        if user:
            if bcrypt.checkpw(self.password.encode("utf-8"), user.password.encode("utf-8")):
                user.created_at = str(user.created_at)
                user.updated_at = str(user.updated_at)
                return user
            else:
                raise KeyError("Authentication failed.")
        else:
            raise LookupError("Account does not exist!")

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

    def save(self):
        """ check email format before executing neo4j model """

        self._validate_email_format()
        if self.find_by_email():
            raise LookupError("Account already exist!")
        else:
            self._hash_password()
            return super(Users, self).save()
