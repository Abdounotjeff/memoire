from django.db import models

# Create your models here.

class AcademicSession(models.Model):
    year = models.CharField(max_length=9, unique=True)  # Example: "2024-2025"
    start_date = models.DateField()
    end_date = models.DateField()


