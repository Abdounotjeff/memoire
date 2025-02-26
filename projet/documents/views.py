from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import *
from quizes.models import Quiz
from results.models import Result
from projetSubmission.models import ProjectSubmission
from projetTask.models import ProjectSubmissionTask
import secrets
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
import ssl
from django.core.mail import get_connection
from django.db.models import Avg, Count, Sum



User = get_user_model()  # Get the CustomUser model

# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Merce d'avoir vérifier votre Email!, tu peux s'incrire maintenant!")
        return redirect('loginPage')
    else:
        messages.error(request, "Lien d'activation est invalide!")
    
    return redirect('index')



def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("pages/user_email.html",{
        'user':user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'http' 
    })

    email = EmailMessage(mail_subject, message, to=[to_email], connection=get_connection())
    if email.send():
        messages.success(request, f'{user}. SVP vérifier votre email : {to_email}.')
    else:
        messages.error(request, f'Something went wrong..., try verifying your email!') 


def resend_verification(request):
    email = request.session.get('pending_email')  # Get email from session

    if not email:
        messages.error(request, "Aucune adresse email trouvée. Inscrivez-vous d'abord.")
        return redirect("registerPage")  # Redirect to registration if no email is found

    try:
        user = User.objects.get(email=email)
        if user.is_active:
            messages.info(request, "Ce compte est déjà activé.")
        else:
            activateEmail(request, user, user.email)
            messages.success(request, "Un nouvel email de vérification a été envoyé !")
    except User.DoesNotExist:
        messages.error(request, "Aucun compte trouvé avec cet email.")

    return render(request, "pages/verify_code.html", {"user_email": email})

def registerPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.is_active=False
            user.save() 
            email = form.cleaned_data.get('email')
            request.session['pending_email'] = email  # Store email in session
            activateEmail(request, user, email)
            return redirect('activ')
        else:
            print(form.errors)  # Debugging: Prints form errors in console
            messages.error(request, 'Form validation failed. Please correct the errors.')
    
    else:  # GET request
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'pages/register.html', context)


def loginPage(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username OR password is incorrect')
    return render(request, 'pages/login.html', context={})


@login_required
def logoutUser(request):
    logout(request)
    return redirect('loginPage')

def activ(request):
    return render(request, 'pages/verify_code.html')

# 📌 PROFESSOR DASHBOARD: Show Groups & Students' Grades
def professor_dashboard(request):
    professor = Professor.objects.get(user=request.user)
    groups = professor.groups.all()

    group_data = []

    for group in groups:
        students = Student.objects.filter(group=group)

        student_data = []
        for student in students:
            # Fetch Quiz Scores (or 0 if not submitted)
            quizzes = Quiz.objects.filter(groups=group)
            quiz_scores = {quiz.id: 0 for quiz in quizzes}  # Default 0

            for quiz in quizzes:
                result = Result.objects.filter(student=student, quiz=quiz).first()
                if result:
                    quiz_scores[quiz.id] = result.score

            # Fetch Project Scores (or 0 if not submitted)
            projects = ProjectSubmissionTask.objects.filter(groups=group)
            project_scores = {project.id: 0 for project in projects}  # Default 0

            for project in projects:
                submission = ProjectSubmission.objects.filter(student=student, task=project).first()
                if submission:
                    project_scores[project.id] = 100  # Example: Full credit if submitted

            student_data.append({
                "student": student,
                "quiz_scores": quiz_scores,
                "project_scores": project_scores,
            })

        group_data.append({"group": group, "students": student_data})

    return render(request, "pages/professor_dashboard.html", {"group_data": group_data})