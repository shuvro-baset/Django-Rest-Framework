from django.db import models
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token

from core.models import BaseModel


class User(AuthUser, BaseModel):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def as_json(self):
        token, created = Token.objects.get_or_create(user=self)
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
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


class Message(BaseModel):
    message = models.TextField()
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
