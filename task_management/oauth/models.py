from django.db import models
from users.models import User
from django.conf import settings
# Create your models here.

class UserDeviceToken(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_device_user'
    )
    token = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.active}'