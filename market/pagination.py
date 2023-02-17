from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination, CursorPagination

#* Page pagination
class ProductsPagination(PageNumberPagination):
    # Amount of results per page
    page_size = 2
    # Allows clients to indicate the page number
    page_query_param = 'page_number'
    # Overwrite the number of results per page.
    page_size_query_param = 'page_size'
    # Define a limit for the number of results
    max_page_size = 5
    # String used to visit the last page
    last_page_strings = 'last'

#* LimitOFFset pagination
class ProductsPaginationOffsetLimit(LimitOffsetPagination):
    default_limit = 2

    # Overwrite the keywords to define the offset and limit
    offset_query_param = 'offset'
    limit_query_param = 'limit'
    max_limit = 5

class ProductsCursorPagination(CursorPagination):
    ordering = '-price'
    page_size = 2
    cursor_query_param = 'record'