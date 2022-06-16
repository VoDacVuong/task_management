from urllib import response
from django.shortcuts import render
from .models import User
from rest_framework.decorators import action
from utils.views import AbstractView, query_debugger, paginate_data
from django.contrib.auth import authenticate
from rest_framework import permissions
import jwt, datetime
from django.conf import settings
from rest_framework.response import Response
from users import app_utils as user_utils
from .serializers import UserSerializer

# Create your views here.

class UserAPI(AbstractView):...
    # permission_classes = [permissions.IsAuthenticated]  
    # @query_debugger
    # @action(methods=['POST'], url_path='login', detail=False)
    # def login(self, request):
    #     try:
    #         data = self.request_handler.handle(request)
    #         email = data.get_body_value('email')
    #         password = data.get_body_value('password')

    #         #validate email
    #         serializer_class = UserSerializer()
    #         serializer_class.validate_email(data={'email': email})

    #         # authentication user
    #         user = user_utils.authentication_(request, email, password)

    #         # set cookies
    #         response = user_utils.set_cookie_(user)

    #         return response
    #     except Exception as exception:
    #         return self.exception_handler.handle(exception)

    # @query_debugger
    # @action(methods=['POST'], url_path='matrix', detail=False)
    # def matrix_user(self, request):
    #     try:
    #         # check cookie
    #         user_utils.check_cookie(request)

    #         # check permission
    #         if request.user.admin == True:...
    #             # to do
    #         import pdb;pdb.set_trace()
    #         users = User.objects.all()

    #         response_data = UserSerializer(users, many=True).data
    #         return self.response_handler.handle(response_data)
    #     except Exception as exception:
    #         return self.exception_handler.handle(exception)
        


