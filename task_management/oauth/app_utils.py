import datetime
from .models import UserDeviceToken

def deactivate_token(user):
    user_device_token = UserDeviceToken.objects.filter(user=user, active=True)
    for entity in user_device_token:
        entity.active = False
        entity.deactivated_at = datetime.datetime.now()

    UserDeviceToken.objects.bulk_update(user_device_token, ['active', 'deactivated_at'])
    