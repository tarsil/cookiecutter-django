import json

from django.db import models
from django.db.models import Field
from django.utils.translation import gettext_lazy as _
from djongo.models.fields import ObjectIdFieldMixin


class GenericObjectIdField(ObjectIdFieldMixin, Field):
    pass


class _ObjectIdField(GenericObjectIdField):
    pass


class ObjectIdField(_ObjectIdField):
    """
    For every document inserted into a collection MongoDB internally creates an field.
    The field can be referenced from within the Model as _id.

    This is internally used as a mapping for _ids and it's not auto_incremental
    """
    pass


class SubList(list):
    def __init__(self, delimiter, *args):
        self.delimiter = delimiter
        super().__init__(*args)

    def __str__(self):
        return self.delimiter.join(self)
