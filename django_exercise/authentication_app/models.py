from django.db import models
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token
from core.models import BaseModel

# user model inherit BaseModel
class User(AuthUser, BaseModel):
    # make username field as email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def as_json(self):
        # create token
        token, created = Token.objects.get_or_create(user=self)
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.first_name + self.last_name,
            "email": self.username,
            "token": token.key
        }

    def __str__(self):
        return (self.first_name + ' ' + self.last_name).strip()

    @classmethod
    def _create_user(cls, email=None, password=None, **extra_fields):
        user = cls(username=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_admin = False
        user.save()
        return user

    @classmethod
    def validate_unique_email(cls, email):
        return True if cls.objects.filter(username=email).exists() else False
