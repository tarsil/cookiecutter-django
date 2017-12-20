import urlparse

from django import http


class TestRequest(http.HttpRequest):
    """Just enough implementation to make it testable"""

    def __init__(self, uri, method='GET'):
        super().__init__()
        self.method = method
        _, self.host, self.path, self.query, _ = urlparse.urlsplit(uri)
        self.META['QUERY_STRING'] = self.query
        self.GET = http.QueryDict(self.query)

    def get_host(self):
        return self.host
