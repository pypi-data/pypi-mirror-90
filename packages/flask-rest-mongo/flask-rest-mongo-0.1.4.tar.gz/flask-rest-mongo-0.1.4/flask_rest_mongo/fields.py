from mongoengine.fields import *
from bson.objectid import ObjectId
from flask_restful.reqparse import Argument
import json
import datetime
ALL_MONGO_FIELDS = [
    "StringField",
    "URLField",
    "EmailField",
    "IntField",
    "LongField",
    "FloatField",
    "DecimalField",
    "BooleanField",
    "DateTimeField",
    "DateField",
    "ComplexDateTimeField",
    "EmbeddedDocumentField",
    "ObjectIdField",
    "GenericEmbeddedDocumentField",
    "DynamicField",
    "ListField",
    "SortedListField",
    "EmbeddedDocumentListField",
    "DictField",
    "MapField",
    "ReferenceField",
    "CachedReferenceField",
    "LazyReferenceField",
    "GenericLazyReferenceField",
    "GenericReferenceField",
    "BinaryField",
    "GridFSError",
    "GridFSProxy",
    "FileField",
    "ImageGridFsProxy",
    "ImproperlyConfigured",
    "ImageField",
    "GeoPointField",
    "PointField",
    "LineStringField",
    "PolygonField",
    "SequenceField",
    "UUIDField",
    "MultiPointField",
    "MultiLineStringField",
    "MultiPolygonField",
    "GeoJsonBaseField",
]
    


class MixField(object):
    """
    docstring
    """

    def __init__(self):
        pass
    def __call__(self, value):
        return value


class MixObjectID(MixField):

    def __call__(self, value):
        return ObjectId(value)

class MixRef(MixField):

    def __init__(self, document_type=None):
        self.document_type = document_type
    
    def _get_ref_obj(self, key):
        id_field = self.document_type._meta['id_field']
        obj = self.document_type.objects(**{id_field:key}).first()
        return obj

    def __call__(self, key):
        return self._get_ref_obj(key)

class MixList(MixRef):
    
    def __init__(self, field=None):
        self.field = field
        self.document_type = None
        if field is not None:
            self.document_type = field.document_type
    def __call__(self, value):
        if self.document_type is None:
            return value
        else:
            obj = self._get_ref_obj(value)
            return obj
        return value

class MixDict(MixField):
    """
    docstring
    """
    def __call__(self, value):
        if isinstance(value, str):
            return json.loads(value)
        return value



class MixDate(MixField):

    def __call__(self, value):
        return datetime.date.fromisoformat(value)

class MixDateTime(MixField):

    def __call__(self, value):
        return datetime.datetime.fromisoformat(value)

def type_trans(field):
    pass

def parser_field(name, field, **kws):
    if isinstance(field, (StringField, EmailField, URLField)):
        return Argument(name, type=str, **kws)
    if isinstance(field, (ObjectId, ObjectIdField)):
        return Argument(name, type=MixObjectID(), **kws)
    if isinstance(field, (IntField, LongField)):
        return Argument(name, type=int, **kws)
    if isinstance(field, (BooleanField,)):
        return Argument(name, type=bool, **kws)
    if isinstance(field, (FloatField, DecimalField)):
        return Argument(name, type=float, **kws)
    if isinstance(field, (ListField,)):
        return Argument(name, type=MixList(field.field), action='append', **kws)
    if isinstance(field, (DictField, PointField, GeoJsonBaseField)):
        return Argument(name, type=MixDict(), **kws)
    if isinstance(field, ReferenceField):
        return Argument(name, type=MixRef(field.document_type), **kws)
    if isinstance(field, DynamicField):
        return Argument(name, type=MixField(), action='append', **kws)
    if isinstance(field, DateField):
        return Argument(name, type=MixDate(), **kws)
    if isinstance(field, DateTimeField):
        return Argument(name, type=MixDateTime(), **kws)
    return Argument(name, type=str)