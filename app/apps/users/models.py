import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.users.managers import UserManager

from rest_framework_simplejwt.tokens import RefreshToken

AUTH_PROVIDERS = {'email': 'email', 'google': 'google', 'github': 'github', 'linkedin': 'linkedin'}


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    given_name = models.CharField(max_length=30, blank=True)
    family_name = models.CharField(max_length=30, blank=True)
    mobile_number = models.CharField(max_length=8, null=True, blank=True, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=50, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['given_name', 'family_name', 'mobile_number']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    def get_session(self):
        tokens = self.get_tokens()

        return {
            'email': self.email,
            'given_name': self.given_name,
            'family_name': self.family_name,
            "access": str(tokens.get('access')),
            "refresh": str(tokens.get('refresh'))
        }


class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otc = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.email} - otc"
