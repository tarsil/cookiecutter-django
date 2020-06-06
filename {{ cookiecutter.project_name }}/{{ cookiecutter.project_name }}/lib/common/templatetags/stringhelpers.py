import re
from django import template

from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

is_char = re.compile(r"[a-zA-Z0-9]")

nbsp_regex = re.compile(r'&nbsp;')
htmle_regex = re.compile(r'&[a-zA-Z0-9]{2,8};')
link_regex = re.compile(r'(([a-zA-Z]+)://[^ \t\n\r]+)', re.MULTILINE)

@register.filter_function
def truncatechars_nospace(string, length):
    string = string.rstrip()

    if len(string) <= length:
        return string

    ret = string[:length].rstrip()

    if ret[-1:][0] in ",":
        ret = ret[:-1]

    elif is_char.match(ret[-1:][0]):
        ret += "..."

    return ret


@register.filter_function
def no_trailing_ellipsis(string):
    if string.endswith('...'):
        return string[:3]

    return string

@register.filter_function
def append(string1, string2):
    return "%s%s" % (string1, string2)


@register.filter_function
def strip_html_entities(string):

    string = re.sub(nbsp_regex, ' ', string)
    string = re.sub(htmle_regex, '', string)

    return string


@register.filter()
def htmlentities(s):
    return mark_safe(escape(s).encode('ascii', 'xmlcharrefreplace'))


@register.filter_function
def linkify(value):

    def _spacify(s, chars=100):
        if len(s) <= chars:
            return s
        for k in range(len(s) / chars):
            pos = (k + 1) * chars
            s = s[0:pos] + ' ' + s[pos:]
        return s

    def _replace(match):
        href = match.group(0)
        return '<a href="%s" class="external" rel="nofollow" target="_blank">%s</a>' % (href, _spacify(href))

    return link_regex.sub(_replace, value)
