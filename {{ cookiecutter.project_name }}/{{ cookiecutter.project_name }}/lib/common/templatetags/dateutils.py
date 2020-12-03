from django.template import Library, TemplateSyntaxError


register = Library()


@register.filter
def week_number(value):
    """

    Args:
      value:

    Returns:

    """
    try:
        return value.strftime('%W')
    except AttributeError:
        raise TemplateSyntaxError('week_number filter must be passed a datetime-like object!')
