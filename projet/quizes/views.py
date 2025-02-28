from django.shortcuts import render
from django.views.generic import ListView
from .models import Quiz
from django.http import JsonResponse
from questions.models import Question, Answer
from results.models import Result
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuizForm
# Create your views here .

class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'

def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    context = {
        'obj': quiz
    }
    return render(request, 'quizes/quiz.html', context)

def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q):answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time
    })

def save_quiz_view(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists()) #we removed csrftoken from the data resutls by transfoming it to a proper dict

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            question = Question.objects.get(text = k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        score = 0
        multiplier = 100/quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            if a_selected !="":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score +=1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append({str(q) : {'correct Answer': correct_answer, 'answered' : a_selected}})
            else:
                results.append({str(q): 'not answered'})
        
        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_>=quiz.required_score:
            return JsonResponse({'passed': True, 'score':score_ , 'results':results})
        else:
            return JsonResponse({'passed': False, 'score':score_ , 'results':results})
        
@login_required
def create_quiz(request):
    if request.user.role != "professor":
        return redirect('index')  # Prevent students from accessing

    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quizzes')  # Redirect to quiz list
    else:
        form = QuizForm()

    return render(request, 'quizes/createQuiz.html', {'form': form})
