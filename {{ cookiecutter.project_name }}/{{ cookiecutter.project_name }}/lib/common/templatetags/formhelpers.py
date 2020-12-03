from django import forms
from django.template import Library

register = Library()


def get_current_choice_field_value(bound_field):
    """

    Args:
      bound_field:

    Returns:

    """
    choices = list(bound_field.field.choices)
    current_value = bound_field.value()

    try:
        selected_choice = [label for value, label in choices if str(value) == str(current_value)][0]
        return selected_choice
    except IndexError:
        return bound_field.label


@register.simple_tag
def field_text_value(bound_field):
    """

    Args:
      bound_field:

    Returns:

    """
    if isinstance(bound_field.field, forms.ChoiceField):
        return get_current_choice_field_value(bound_field)

    elif isinstance(bound_field.field, forms.CharField):
        return bound_field.value()

    return bound_field.label


@register.filter
def fieldtype(obj):
    """

    Args:
      obj:

    Returns:

    """
    return obj.__class__.__name__
