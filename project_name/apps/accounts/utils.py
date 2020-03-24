import uuid

import accounts.models
from slugify import slugify


def get_uuid():
    """
    Generate an UUID for the HubUser
    :return: uuid
    """
    _uuid = str(uuid.uuid4())
    hub_user = accounts.models.HubUser.objects.filter(uuid=_uuid)
    if hub_user.exists():
        get_uuid()
    return _uuid


def generate_username(first_name):
    uuid_user = str(uuid.uuid4())
    username = first_name.lower() + "-{id}".format(id=uuid_user[:12])
    return username


def update_hub_user_slug(hub_user):
    try:
        slug = slugify(hub_user.user.username)
        hub_user.slug = slug
        hub_user.save()
        return hub_user
    except accounts.models.HubUser.DoesNotExist:
        pass
