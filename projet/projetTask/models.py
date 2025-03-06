from django.db import models
from documents.models import Professor
from groupe.models import Group
from django.utils.timezone import now
# Create your models here.

class ProjectSubmissionTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def is_active(self):
        return self.start_time <= now() <= self.end_time
    
    def __str__(self):
        return self.title