from django.contrib.auth.models import AbstractUser,User
from django.db import models
import secrets
from django.conf import settings

class CustomUser(AbstractUser):
    # Add additional fields if needed
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.username




