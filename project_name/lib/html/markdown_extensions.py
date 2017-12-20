"""
Based on: https://github.com/bhch/markdown-nofollow
"""
import re
from markdown import Extension
from markdown.inlinepatterns import LinkPattern, LINK_RE
from django.conf import settings

BASE_URL = "^(https|http)://%s" % settings.CANONICAL_SITE_URL


def is_href_external(href):
    if not href:
        return False
    if href.startswith('/') or re.match(BASE_URL, href):
        return False
    return True


class NofollowMixin(object):

    def handleMatch(self, m):
        element = super().handleMatch(m)
        if element is not None and is_href_external(element.get('href')):
            element.set('rel', 'nofollow')
        return element


class TargetBlankMixin(object):

    def handleMatch(self, m):
        element = super().handleMatch(m)
        if element is not None and is_href_external(element.get('href')):
            element.set('target', '_blank')
        return element


class ExternalLinkPattern(NofollowMixin, TargetBlankMixin, LinkPattern):
    pass


class ExternalLinkExtensions(Extension):

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['link'] = ExternalLinkPattern(LINK_RE, md)
