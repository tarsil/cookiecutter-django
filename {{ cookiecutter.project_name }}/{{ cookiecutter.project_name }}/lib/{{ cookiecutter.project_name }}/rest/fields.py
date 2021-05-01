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
