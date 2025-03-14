from django.db import models
import random
from documents.models import Professor
from groupe.models import Group
from django.utils.timezone import now
# Create your models here.

DIFF_CHOICES =(
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)

class Quiz(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of quiz in Minutes")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)
    required_score = models.IntegerField(help_text="required score to pass the quiz")
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE)
    start_time = models.DateTimeField()  # Students can access from this time
    end_time = models.DateTimeField()  # Access closes after this time
    groups = models.ManyToManyField(Group)  # Assign quiz to multiple groups
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}-{self.topic}"
    
    class Meta:
        verbose_name_plural = "Quizes"

    def get_questions(self): #to get all question to the quiz
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]
    
    def is_active(self):
        return self.start_time <= now() <= self.end_time