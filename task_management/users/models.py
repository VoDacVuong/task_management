import uuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email)
        )

        user.set_password(password)
        user.active = False
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )

        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )

        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()

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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    username = models.CharField(max_length=255, unique=True)

    first_name = models.CharField(max_length=128)

    last_name = models.CharField(max_length=128)

    admin = models.BooleanField(default=False)  # a superuser
    staff = models.BooleanField(default=False)  # a admin user; non super-user

    last_login = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    joined_at = models.DateTimeField(
        auto_now=False, auto_now_add=True
    )

    locked = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def __str__(self) -> str:
        return f'{self.username}'

