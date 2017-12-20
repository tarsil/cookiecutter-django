import markdown
from bs4 import BeautifulSoup
import premailer

from django.conf import settings
from lib.html.markdown_extensions import ExternalLinkExtensions


def absolutize_email_content(content):
    content = content.strip()

    if not len(content):
        return ''

    base_url = "https://%s" % settings.CANONICAL_SITE_URL
    transformed_content = premailer.transform(content, base_url=base_url)

    soup = BeautifulSoup.BeautifulSoup(transformed_content)

    return ''.join([unicode(x) for x in soup.body.contents])


def absolutize_link(link):
    protocol = 'http'
    if settings.SECURE_SSL_REDIRECT:
        protocol = 'https'
    return "{protocol}://{host}{link}".format(
        protocol=protocol, host=settings.CANONICAL_SITE_URL, link=link
    )


def get_html_from_markdown(markdown_content, strip_paragraph=False):
    if markdown_content:
        content = markdown.markdown(markdown_content, extensions=[ExternalLinkExtensions()])
    else:
        return u""

    content = content.strip()
    if not strip_paragraph:
        return content

    if content.startswith('<p>') and content.endswith('</p>'):
        return content[3:-4]
    return content
