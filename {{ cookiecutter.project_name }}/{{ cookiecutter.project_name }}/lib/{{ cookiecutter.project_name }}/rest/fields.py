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
        """

        Args:
          obj:

        Returns:

        """
        return self._choices[obj]

    def to_internal_value(self, data):
        """

        Args:
          data:

        Returns:

        """
        return getattr(self._choices, data)
 

class WritableSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        super().__init__(**kwargs)

        self.read_only = False

    def get_default(self):
        default = super().get_default()

        return {self.field_name: default}

    def to_internal_value(self, data):
        return {self.field_name: data}

