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

class UserAPI(AbstractView):
    # permission_classes = [permissions.IsAuthenticated]
    @query_debugger
    @action(methods=['POST'], url_path='matrix', detail=False)
    def matrix_user(self, request):
        try:
            # import pdb;pdb.set_trace()
            # check cookie
            user_utils.check_cookie(request)

            # check permission
            if request.user.admin == True:...
                # to do
            # import pdb;pdb.set_trace()
            users = User.objects.all()

            response_data = UserSerializer(users, many=True).data
            # import pdb;pdb.set_trace()
            return self.response_handler.handle(response_data)
        except Exception as exception:
            return self.exception_handler.handle(exception)
        


