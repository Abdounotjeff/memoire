from django.contrib.auth.models import AbstractUser,User
from django.db import models
import secrets
from django.conf import settings
from groupe.models import Group


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'student'),
        ('professor', 'professor'),
        ('admin', 'admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='professor')
    is_active = models.BooleanField(default=False)

    def is_student(self):
        return self.role == 'student'
    
    def is_professor(self):
        return self.role == 'professor'
    
    
    
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.user.username


class Professor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.user.username
