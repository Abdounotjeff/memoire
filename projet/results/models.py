from django.db import models
from quizes.models import Quiz
from django.conf import settings  # ✅ Import settings instead of User

# Create your models here.
class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ Use AUTH_USER_MODEL
    score = models.IntegerField()

    def __str__(self):
        return str(self.pk)

