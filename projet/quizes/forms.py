from django import forms
from .models import Quiz

DIFF_CHOICES =(
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            'name', 'topic', 'number_of_questions', 'time', 
            'difficulty', 'required_score', 'start_time', 'end_time', 'groups'
        ]
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'difficulty': forms.Select(choices=DIFF_CHOICES),
            'groups': forms.CheckboxSelectMultiple(),  # Allow multiple group selection
        }

    def __init__(self, *args, **kwargs):
        professor = kwargs.pop('professor', None)  # Get the logged-in professor
        super().__init__(*args, **kwargs)
        
        if professor:
            # Limit groups to only those assigned to the professor
            self.fields['groups'].queryset = professor.groups.all()

    def save(self, commit=True, professor=None):
        quiz = super().save(commit=False)
        if professor:
            quiz.created_by = professor  # Assign the logged-in professor
        if commit:
            quiz.save()
            self.save_m2m()  # Save ManyToMany relationships
        return quiz