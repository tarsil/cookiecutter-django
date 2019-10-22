# pragma: no cover
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import pagination
from rest_framework.response import Response


class Pagination(pagination.PageNumberPagination):
    """
    Custom paginator for REST API responses
    'links': {
               'next': next page url,
               'previous': previous page url
            },
            'count': number of records fetched,
            'total_pages': total number of pages,
            'next': bool has next page,
            'previous': bool has previous page,
            'results': result set
    })
    """

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'pagination': {
                'previous_page': self.page.number - 1 if self.page.number != 1 else None,
                'current_page': self.page.number,
                'next_page': self.page.number + 1 if self.page.has_next() else None,
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'next': self.page.has_next(),
            'previous': self.page.has_previous(),
            'results': data
        })


def paginator(request, queryset=None, number_per_page=10):
    """
    Returns the custom paginator for the django custom admin pages
    :param request: The request of a page
    :param queryset: The queryset to calculate the number of pages
    :param number_per_page: Number of results per page
    :return: paginator
    """
    paginator = Paginator(queryset, number_per_page)
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return pages
