from rest_framework.pagination import PageNumberPagination


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class AppPagination(PageNumberPagination):
    page_size = 7
    page_size_query_param = "page-size"
    max_page_size = 100

class CommonPagination(PageNumberPagination):
    page_size = 10000
    page_size_query_param = 'page_size'
    max_page_size = 100



class BaseViewMixin:
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    
    pagination_class = CommonPagination