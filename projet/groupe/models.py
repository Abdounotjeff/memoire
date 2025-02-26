from django.db import models
from SessionAcademique.models import AcademicSession
# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.academic_session.year})"
