from django.db import models

"""
Package that allow the whole project to use common functions as a resource
"""

class TimeStampedModel(models.Model):
    """
    An Abstract Base Class provides self-updating `create` and `modified` fields, for every model
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
