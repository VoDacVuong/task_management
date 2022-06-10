import string
import time
import logging
import functools
from abc import ABC
from datetime import datetime
import random

from django.http import JsonResponse, response
from django.db import connection, reset_queries
from django.core.exceptions import (
    ValidationError,
    FieldError
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import viewsets
from rest_framework.decorators import action

from . import messages, exceptions


PAGE_SIZE = 10
PAGE_SIZE_MAX = 40


def paginate_data(request, data):
    '''
    Function to handle pagination data.

    Params:

    data: array data.

    request: request object that contain paginate info

    page: page to show (Default is 1).

    page_size: Defaults is 10 (PAGE_SIZE=10).

    Return a JSON data:

    response_data = {
        "totalRows": total,
        "totalPages": total_pages,
        "currentPage": page_number,
        "content": content
    }
    '''

    page = int(request.data.get('page', 1))
    page_size = int(request.data.get('page_size', PAGE_SIZE))

    # Handle page_size = 'all'
    # page_size = 0 for get all
    if page_size == 0:
        page_size = len(data) + 1
    elif page_size < 0:
        raise ValueError(messages.NEGATIVE_PAGE_SIZE)
    elif page_size > PAGE_SIZE_MAX:
        raise ValueError(messages.OVER_PAGE_SIZE_MAX + PAGE_SIZE_MAX)

    paginator = Paginator(data, page_size)

    total_pages = paginator.num_pages

    if int(total_pages) < page:
        page_number = page
        content = []
    else:
        current_page = paginator.page(page)
        page_number = current_page.number
        content = current_page.object_list

    total = paginator.count

    response_data = {
        "totalRows": total,
        "totalPages": total_pages,
        "currentPage": page_number,
        "content": content,
        "pageSize": page_size
    }

    return response_data


class JsonResponseHandler:
    @classmethod
    def handle(cls, data=None, error_code=0, message=messages.SUCCESS) -> JsonResponse:
        return JsonResponse(
            data={
                'data': data,
                'error_code': error_code,
                'message': message,
                "current_time": datetime.now(),
            }
        )


class ExceptionHandler:

    @classmethod
    def _get_code_and_message(cls, exception: Exception) -> set:
        print('=== type: ', type(exception), '=== ex: ', exception)

        default_message = (500, '{}. {}'.format(
            str(exception),
            messages.CONTACT_ADMIN_FOR_SUPPORT
        ))
        switcher = {
            exceptions.ValidationException: (400, str(exception)),
            exceptions.InvalidArgumentException: (400, str(exception)),
            exceptions.NotFoundException: (404, str(exception)),
            exceptions.AuthenticationException: (401, str(exception)),
            ValidationError: (400, messages.INVALID_ARGUMENT),
            ValueError: (400, str(exception)),
            FieldError: (400, messages.FIELD_NOT_SUPPORT),
            KeyError: (400, messages.FIELD_NOT_SUPPORT),
            exceptions.NetworkException: (500, str(exception)),
        }

        return switcher.get(type(exception), default_message)

    @classmethod
    def handle(cls, exception: Exception) -> JsonResponse:
        error_code, message = cls._get_code_and_message(exception)

        return JsonResponse(
            data={
                'data': None,
                'error_code': error_code,
                'message': message,
                "current_time": datetime.now(),
            }
        )


# Calculate query time and number of query statement
def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print("Function : " + func.__name__)
        print("Number of Queries : {}".format(end_queries - start_queries))
        print("Finished in : {}".format(end - start))
        print("======================================")

        return result

    return inner_func


class RequestExtractor:
    def __init__(self, request):
        self.__request = request

    def get_body_value(self, key, default=None):
        form_data_param = self.__request.POST.get(key, default)
        json_data_param = self.get_json_body_value(key, default)
        return form_data_param or json_data_param

    def get_para_value(self, key, default=None):
        return self.__request.GET.get(key, default)

    def get_file_input(self, key, default=None):
        return self.__request.FILES.get(key, default)

    def get_list_file_input(self, key, default=None):
        return self.__request.FILES.getlist(key, default)

    def get_json_body_value(self, key, default=None):
        return self.__request.data.get(key, default)


class RequestHandler:
    @classmethod
    def handle(cls, request):
        return RequestExtractor(request)


class PagingHandler:
    @classmethod
    def handle(cls, request, data=[]):
        return paginate_data(request, data)


class AbstractView(viewsets.GenericViewSet):
    response_handler = JsonResponseHandler
    exception_handler = ExceptionHandler
    request_handler = RequestHandler
    paging_handler = PagingHandler


