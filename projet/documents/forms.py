from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from quizes.models import Quiz
from questions.models import Question, Answer
from documents.models import Professor
from groupe.models import Group

class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        common_classes = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 shadow-sm'

        self.fields['username'].widget.attrs.update({
            'class': common_classes,
            'placeholder': "Entrez votre nom d'utilisateur"
        })
        self.fields['email'].widget.attrs.update({
            'class': common_classes,
            'placeholder': "Entrez votre adresse e-mail"
        })
        
        # Manually override password fields
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': common_classes,
            'placeholder': "Entrez votre mot de passe"
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': common_classes,
            'placeholder': "Confirmez votre mot de passe"
        })

# Difficulty choices for the quiz
DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)

class QuizForm(forms.ModelForm):
    # Custom fields for dynamically added questions and answers
    questions = forms.CharField(widget=forms.HiddenInput(), required=False)
    answers = forms.CharField(widget=forms.HiddenInput(), required=False)
    correct_answers = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Quiz
        fields = [
            'name', 'topic', 'number_of_questions', 'time', 
            'difficulty', 'required_score', 'start_time', 'end_time', 'groups',
            'questions', 'answers', 'correct_answers'  # Include custom fields
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

            # Process questions and answers
            questions = self.cleaned_data.get('questions', '[]')
            answers = self.cleaned_data.get('answers', '[]')
            correct_answers = self.cleaned_data.get('correct_answers', '[]')

            if questions and answers and correct_answers:
                import json
                questions = json.loads(questions)
                answers = json.loads(answers)
                correct_answers = json.loads(correct_answers)

                for i, question_text in enumerate(questions):
                    if question_text.strip():
                        question = Question.objects.create(
                            quiz=quiz,
                            text=question_text,
                            created=quiz.created_at  # Use quiz creation time
                        )

                        # Get answers for this question
                        answer_texts = answers[i * 4:(i + 1) * 4]  # Assuming 4 answers per question
                        correct_answer_index = correct_answers[i] if i < len(correct_answers) else 0

                        for j, answer_text in enumerate(answer_texts):
                            if answer_text.strip():
                                Answer.objects.create(
                                    question=question,
                                    text=answer_text,
                                    correct=(j == correct_answer_index),
                                    created=quiz.created_at  # Use quiz creation time
                                )
        return quiz