from django.conf import settings
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_sitemap_href(context):
    """

    Args:
      context:

    Returns:

    """
    request = context.get('request')
    if request:
        host = request.get_host()
    else:
        host = settings.CANONICAL_SITE_URL
    return 'https://%s/sitemap.xml' % host


@register.inclusion_tag('_meta/language_alternatives.html', takes_context=True)
def get_language_alternatives(context):
    """

    Args:
      context:

    Returns:

    """

    lang_domains = []
    for language, host in settings.AF_SITEMAPS:
        lang_domains.append({'lang': language, 'host': host})
    return {
        'request': context.get('request'),
        'lang_domains': lang_domains
    }
