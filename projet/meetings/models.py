from django.db import models
from documents.models import Professor
from groupe.models import Group
from django.utils.timezone import now
# Create your models here.

class meeting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(help_text="recommand using Google meet")
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def is_active(self):
        return self.start_time <= now() <= self.end_time
    
    def __str__(self):
        return self.title