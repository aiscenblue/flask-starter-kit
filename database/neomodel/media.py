from neomodel import (StructuredNode, UniqueIdProperty, RelationshipTo, StringProperty, DateTimeProperty)
from database.neo4j.neomodel.edges.timestamp import EdgeRelationship
from database.neo4j.neomodel.users import Users
from werkzeug.utils import secure_filename
import datetime
import os


class Media(StructuredNode):
    uid = UniqueIdProperty()
    url = StringProperty(required=True)
    user = RelationshipTo(Users, "UPLOADED_BY", model=EdgeRelationship)
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    deleted_at = DateTimeProperty(required=False, default=None)

    def __init__(self):
        super().__init__(self)
        self.__extensions = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

    @property
    def extensions(self):
        return self.__extensions

    @extensions.setter
    def extensions(self, x):
        if isinstance(x, list):
            self.__extensions = x
        else:
            raise ValueError('Invalid format!')

    @extensions.deleter
    def extensions(self):
        del self.__extensions

    def allowed_file(self, filename):
        allowed_extensions = self.extensions
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    def upload(self, files, directory=None):
        t = datetime.datetime.now()
        directory = 'media/default/{}'.format(t.strftime('%Y/%m/%d')) if directory is None else directory
        # check if the post request has the file part
        print(files)
        if 'files' not in files:
            raise ValueError('No file part')

        for file in files.getlist('files'):
            # if user does not select file, browser also
            __filename = file.name or file.filename
            # submit a empty part without filename
            if __filename:
                raise FileNotFoundError('No selected file')
            if file and self.allowed_file(__filename):
                filename = secure_filename('{}-{}'.format(t.strftime('%H-%M-%S'), __filename.lower()))
                if not os.path.exists(directory):
                    os.makedirs(directory)
                file.save(os.path.join(directory, filename))
            else:
                """ skip the unwanted file """
                pass
            #     raise ValidationError('File not allowed!')
        return ['/{}/{}-{}'.format(directory, t.strftime('%H-%M-%S'), file.filename.lower()) for file in files.getlist('files')]