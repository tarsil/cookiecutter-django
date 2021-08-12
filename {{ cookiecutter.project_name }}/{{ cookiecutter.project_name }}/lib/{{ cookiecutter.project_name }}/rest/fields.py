"""
Custom fields added to Retools
"""
from rest_framework import serializers


class ChoicesField(serializers.Field):
    """Choices Field to handle properly with it"""
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super().__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        return getattr(self._choices, data)
 

class WritableSerializerMethodField(serializers.SerializerMethodField):
    """
    Allows the serializer method field to be writable.
    """

    def __init__(self, method_name=None, **kwargs):
        super().__init__(**kwargs)

        self.read_only = False

    def get_default(self):
        default = super().get_default()

        return {self.field_name: default}

    def to_internal_value(self, data):
        return {self.field_name: data}


class AbsoluteImageField(serializers.ImageField):
    """
    Returns the absolute path of a image object
    """

    def to_representation(self, value):
        if not value:
            return None

        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(value.url)
        return value.url

