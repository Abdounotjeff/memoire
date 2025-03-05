from django.db import models
from documents.models import Student
from projetTask.models import ProjectSubmissionTask
from django.utils.timezone import now
# Create your models here.

class ProjectSubmission(models.Model):
    task = models.ForeignKey(ProjectSubmissionTask, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file = models.FileField(upload_to="projects/") #don't forget to add a dateTime system to folder naming
    grade = models.IntegerField(null=True, blank=True, default=0)  # Allow professor to manually enter grades
    def __str__(self):
        return f"{self.student.user.username} - {self.task.title}"