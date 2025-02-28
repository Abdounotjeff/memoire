from django.db import models
from documents.models import Professor
from groupe.models import Group
from django.utils.timezone import now
# Create your models here.

class ProjectSubmissionTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae,")
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def is_active(self):
        return self.start_time <= now() <= self.end_time
    
    def __str__(self):
        return self.title