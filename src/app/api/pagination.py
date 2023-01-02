from rest_framework.pagination import PageNumberPagination


class AppPagination(PageNumberPagination):
    page_size_query_param = "page_size"
