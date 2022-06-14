from drf_yasg import openapi

book_matrix_swagger_params = [
    openapi.Parameter('name', in_=openapi.IN_BODY, type=openapi.TYPE_STRING),
]