from django.db import models
from quizes.models import Quiz
from django.conf import settings  # ✅ Import settings instead of User
from documents.models import Student

# Create your models here.
class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # ✅ Use AUTH_USER_MODEL
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.quiz.name}: {self.score}"

