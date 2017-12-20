from django.template import Library
from django import forms

register = Library()


def get_current_choice_field_value(bound_field):
    choices = list(bound_field.field.choices)
    current_value = bound_field.value()

    try:
        selected_choice = [label for value, label in choices if str(value) == str(current_value)][0]
        return selected_choice
    except IndexError:
        return bound_field.label


@register.assignment_tag(name='get_field_text_value')
@register.simple_tag
def field_text_value(bound_field):
    if isinstance(bound_field.field, forms.ChoiceField):
        return get_current_choice_field_value(bound_field)

    elif isinstance(bound_field.field, forms.CharField):
        return bound_field.value()

    return bound_field.label

@register.filter
def fieldtype(obj):
    return obj.__class__.__name__