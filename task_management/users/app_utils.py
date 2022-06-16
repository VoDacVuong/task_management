from .models import User
from django.contrib.auth import authenticate
from utils import exceptions, messages
from rest_framework.response import Response
import jwt, datetime
from django.conf import settings
from oauth.models import UserDeviceToken
from oauth import app_utils as oauth_utils

def authentication_(request, email, password):
    user = authenticate(request = request, email = email, password = password)
    if not user:
        raise exceptions.InvalidArgumentException(message=messages.USER_NOT_FOUND)
    return user

def set_cookie_(user):
    payload = {
        'id': str(user.id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=50),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY).decode('utf-8')
    response = Response()
    response.set_cookie(key='user', value=token, httponly=True)
    response.data = {
        'data': payload,
        'error_code': 200,
        'message': 'Success',
        'current_time': datetime.datetime.now()
    }
    
    # deactive old token
    oauth_utils.deactivate_token(user)

    UserDeviceToken.objects.create(
        user = user,
        token = token,
        active = True
    )

    return response

def check_cookie(request):
    user = request.COOKIES.get('user')
    payload = jwt.decode(user, settings.SECRET_KEY)
    try:
        user = User.objects.get(pk=payload['id'])
        request.user = user
    except Exception as exception:
        pass
    
