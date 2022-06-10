from statistics import mode
import uuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)
# Create your models here.

class User(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, unique=True,
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=128,
        unique=True,
    )

    # password = models.CharField(_("password"), max_length=128),

    first_name = models.CharField(max_length=128)

    last_name = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    modified_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        return super(User, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.username}'

