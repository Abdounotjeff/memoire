from django.db import models

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
    time = models.IntegerField(help_text="duration of quiz in seconds")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)
    required_score = models.IntegerField(help_text="required score to pass the quiz")

    def __str__(self):
        return f"{self.name}-{self.topic}"
    
    class Meta:
        verbose_name_plural = "Quizes"

    def get_questions(self): #to get all question to the quiz
        return self.question_set.all()[:self.number_of_questions]