from django.db import models
from authentication_app.models import User
from core.models import BaseModel


# message model
class Message(BaseModel):
    message = models.TextField()
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
