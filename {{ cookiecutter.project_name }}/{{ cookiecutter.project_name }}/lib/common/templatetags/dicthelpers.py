from django import template

register = template.Library()


@register.filter(name="getkey")
def getkey(value, key):
    """\
    Fetch a key from a value. Useful for cases such as dicts which have '-' and ' '
    in the key name, which Django can't cope with via the standard '.' lookup.
    """
    try:
        return value[key]
    except KeyError:
        return ""


@register.filter(name="delkey")
def delkey(value, key):
    """
    :param value: dictionary
    :param key: string - name of element to delete
    """
    value.pop(key)
    return ""
