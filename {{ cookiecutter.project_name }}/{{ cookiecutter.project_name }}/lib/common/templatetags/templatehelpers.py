import re
import random

from django.template import Library
from django.template.loader import render_to_string, get_template
from django.utils.safestring import mark_safe

register = Library()


SPACE_REGEX = re.compile('\s+')


@register.simple_tag(takes_context=True)
def render_stripped_contents(context, template):
    rendered = render_to_string(template, context)

    return re.sub(SPACE_REGEX, ' ', rendered)


@register.simple_tag(takes_context=True)
def render_as_template(context, string):
    template = get_template(string)
    return mark_safe(
        template.render(context)
    )


@register.simple_tag
def get_random_integer(minimum, maximum):
    return random.randint(minimum, maximum)
