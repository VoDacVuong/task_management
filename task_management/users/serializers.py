

import re
from rest_framework import serializers
from .models import User
from utils.views import exceptions, messages


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
        ]
    def validate_email(self, data):
        email = serializers.EmailField()
        EMAIL_PATTERN = '^[a-zA-Z0-9](([.]{1}|[_]{1}|[-]{1}|[+]{1})?[a-zA-Z0-9])*[@]([a-z0-9]+([.]{1}|-)?)*[a-zA-Z0-9]+[.]{1}[a-z]{2,253}$'
        if bool(re.match(EMAIL_PATTERN, data['email'])):
            return data
        raise exceptions.InvalidArgumentException(message=messages.INVALID_EMAIL)