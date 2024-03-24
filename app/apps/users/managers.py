import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        _id = uuid.uuid4()

        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(id=_id, email=email, **extra_fields)

        user.set_password(password)

        user.given_name = extra_fields.get('given_name', '')
        user.family_name = extra_fields.get('family_name', '')
        user.mobile_number = extra_fields.get('mobile_number', '')

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if extra_fields.get("is_verified") is not True:
            raise ValueError(_("Superuser must have is_verified=True."))

        return self.create_user(email, password, **extra_fields)
