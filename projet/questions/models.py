from django.db import models
from quizes.models import Quiz
# Create your models here.

class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)
    
    def get_answers(self):#get all the answers to a particular answer
        return self.answer_set.all() # we can also type the attribute relation name but 
                                     # we need add a related name to question attribute
    
class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}. answer: {self.text}. correct :{self.correct} "