from django.db import models


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateField(auto_now=True, null=True, blank=True)
    enable = models.BooleanField(default=True)

    class Meta:
        abstract = True