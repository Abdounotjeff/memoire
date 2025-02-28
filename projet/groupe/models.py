from django.db import models
from SessionAcademique.models import AcademicSession
# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100)
    academic_level = models.CharField(
        max_length=50, 
        choices=[
            ("1st Year", "1st Year"),
            ("2nd Year", "2nd Year"),
            ("3rd Year", "3rd Year"),
            ("Master 1", "Master 1"),
            ("Master 2", "Master 2"),
        ],
        default="1st Year"
    )

    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.academic_level} - {self.academic_session.year}"
