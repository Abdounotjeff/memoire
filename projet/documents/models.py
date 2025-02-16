from django.contrib.auth.models import AbstractUser,User
from django.db import models
import secrets

class CustomUser(AbstractUser):
    # Add additional fields if needed
    is_professor = models.BooleanField(default=False)
    def __str__(self):
        return self.username

from django.conf import settings
from django.db import models
import secrets

class EmailVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True, default=secrets.token_hex(3))  # 6-char hex code
    verified = models.BooleanField(default=False)


