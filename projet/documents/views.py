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
from django.http import JsonResponse
import json
from questions.models import Question, Answer
from .models import Professor
from groupe.models import Group
from django.utils.timezone import now
from .forms import QuizForm, projectForm
from django.shortcuts import get_object_or_404
from datetime import datetime



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

def send_email_to_student(request, student_email, quiz):
    try:
        user = User.objects.get(email=student_email)
        send_quiz_notification_email(request, user, student_email, quiz)
    except User.DoesNotExist:
        messages.error(request, f"User with email {student_email} does not exist.")

def send_email_to_student_project(request, student_email, projet):
    try:
        user = User.objects.get(email=student_email)
        send_project_notification_email(request, user, student_email, projet)
    except User.DoesNotExist:
        messages.error(request, f"User with email {student_email} does not exist.")

def send_project_notification_email(request, user, to_email, projet):
    mail_subject = f"New project Available: {projet.title}"
    message = render_to_string("pages/studentNotPro.html", {
        'user': user,
        'projet': projet,
        'domain': get_current_site(request).domain,
        'protocol': 'http',  # Change to 'https' if using SSL
    })

    email = EmailMessage(mail_subject, message, to=[to_email], connection=get_connection())
    if email.send():
        messages.success(request, f'Project Task notification sent to {user.first_name} {user.last_name}.')
    else:
        messages.error(request, f'Failed to send Project Task notification to {user.first_name} {user.last_name}.')

def send_quiz_notification_email(request, user, to_email, quiz):
    mail_subject = f"New Quiz Available: {quiz.name}"
    message = render_to_string("pages/studentNot.html", {
        'user': user,
        'quiz': quiz,
        'domain': get_current_site(request).domain,
        'protocol': 'http',  # Change to 'https' if using SSL
    })

    email = EmailMessage(mail_subject, message, to=[to_email], connection=get_connection())
    if email.send():
        messages.success(request, f'Project Task notification sent to {user.first_name} {user.last_name}.')
    else:
        messages.error(request, f'Failed to send Project Task notification to {user.first_name} {user.last_name}.')

def send_email_to_student_delete(request, student_email, quiz):
    try:
        user = User.objects.get(email=student_email)
        send_quiz_notification_email_delete(request, user, student_email, quiz)
    except User.DoesNotExist:
        messages.error(request, f"User with email {student_email} does not exist.")

def send_email_to_student_delete_project(request, student_email, projet):
    try:
        user = User.objects.get(email=student_email)
        send_quiz_notification_email_delete_project(request, user, student_email, projet)
    except User.DoesNotExist:
        messages.error(request, f"User with email {student_email} does not exist.")

def send_quiz_notification_email_delete_project(request, user, to_email, projet):
    mail_subject = f"Project Task removed: {projet.title}"
    message = render_to_string("pages/studentNotDelPro.html", {
        'user': user,
        'projet': projet,
        'domain': get_current_site(request).domain,
        'protocol': 'http',  # Change to 'https' if using SSL
    })

    email = EmailMessage(mail_subject, message, to=[to_email], connection=get_connection())
    if email.send():
        messages.success(request, f'Project Task notification sent to {user.first_name} {user.last_name}.')
    else:
        messages.error(request, f'Failed to send Project Task notification to {user.first_name} {user.last_name}.')


def send_quiz_notification_email_delete(request, user, to_email, quiz):
    mail_subject = f"Quiz Task removed: {quiz.name}"
    message = render_to_string("pages/studentNotDel.html", {
        'user': user,
        'quiz': quiz,
        'domain': get_current_site(request).domain,
        'protocol': 'http',  # Change to 'https' if using SSL
    })

    email = EmailMessage(mail_subject, message, to=[to_email], connection=get_connection())
    if email.send():
        messages.success(request, f'Quiz notification sent to {to_email}.')
    else:
        messages.error(request, f'Failed to send quiz notification to {to_email}.')


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
@login_required
def professor_dashboard(request):
    professor = Professor.objects.get(user=request.user)
    groups = professor.groups.all()

    professor_quizzes = Quiz.objects.filter(created_by=professor)
    professor_projects = ProjectSubmissionTask.objects.filter(created_by=professor)

    group_data = []
    for group in groups:
        students = Student.objects.filter(group=group)
        student_data = []

        for student in students:
            quizzes = Quiz.objects.filter(groups=group)
            quiz_scores = {quiz.id: 0 for quiz in quizzes}
            for quiz in quizzes:
                result = Result.objects.filter(student=student, quiz=quiz).first()
                if result:
                    quiz_scores[quiz.id] = result.score

            projects = ProjectSubmissionTask.objects.filter(groups=group)
            project_scores = {project.id: 0 for project in projects}
            for project in projects:
                submission = ProjectSubmission.objects.filter(student=student, task=project).first()
                if submission:
                    project_scores[project.id] = 100  

            student_data.append({
                "student": student,
                "quiz_scores": quiz_scores,
                "project_scores": project_scores,
            })

        group_data.append({"group": group, "students": student_data})

    context = {
        "group_data": group_data,
        "professor_quizzes": professor_quizzes,
        "professor_projects": professor_projects,
    }

    return render(request, "pages/professor_dashboard.html", context)


@login_required
def create_quiz(request):
    if not request.user.is_professor() or not hasattr(request.user, 'professor'):
        return redirect('index')

    professor = request.user.professor  

    if request.method == "POST":
        form = QuizForm(request.POST, professor=professor)
        if form.is_valid():
            quiz = form.save(professor=professor)  # Save and get quiz instance
            print("saved")
            # Get all students in the selected groups
            students_emails = CustomUser.objects.filter(
            student__group__in=quiz.groups.all(),  # Get students linked to the selected groups
            role="student",  # Ensure they are students
            ).values_list("email", flat=True)  # Extract only emails

            # Convert to a list (if needed)
            students_emails = list(students_emails)
            print("students_emails: ", students_emails)
            for student_email in students_emails:
                send_email_to_student(request, student_email, quiz)

            return redirect('edit_quiz', quiz_id=quiz.id)  # Redirect to edit page
    else:
        form = QuizForm(professor=professor)

    return render(request, 'quizes/createQuiz.html', {'form': form})


#how can i pass from create quiz to edit the just-created quiz

@login_required
def edit_quiz(request, quiz_id):    
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Ensure only the professor who created the quiz can edit it
    if not request.user.is_professor() or quiz.created_by != request.user.professor:
        messages.error(request, "You are not authorized to edit this quiz.")
        return redirect('index')  # Redirect unauthorized users

    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz, professor=request.user.professor)
        if form.is_valid():
            form.save()

            # Handle questions and answers
            questions_texts = request.POST.getlist("questions[]")  # Get all questions
            correct_answers = request.POST.getlist("correct_answers[]")  # Get correct answers

            # Clear existing questions (optional, but be cautious)
            quiz.question_set.all().delete()

            for i, question_text in enumerate(questions_texts):
                if question_text.strip():
                    # Create a new question
                    question = Question.objects.create(
                        quiz=quiz,
                        text=question_text,
                        created=datetime.now()
                    )

                    # Get answers for this question
                    answers_texts = request.POST.getlist(f"answers[{i}][]")
                    
                    # Ensure there's a correct answer for this question
                    if i < len(correct_answers) and correct_answers[i]:
                        correct_answer_index = int(correct_answers[i])
                    else:
                        correct_answer_index = 0  # Default to the first answer if no correct answer is selected

                    for j, answer_text in enumerate(answers_texts):
                        if answer_text.strip():
                            # Create an answer
                            Answer.objects.create(
                                question=question,
                                text=answer_text,
                                correct=(j == correct_answer_index),
                                created=datetime.now()
                            )

            messages.success(request, "Quiz updated successfully!")
            return redirect('professor')  # Redirect to quiz list
    else:
        form = QuizForm(instance=quiz, professor=request.user.professor)

    return render(request, 'quizes/edit_quiz.html', {'form': form, 'quiz': quiz})

@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Ensure only the professor who created the quiz can delete it
    if not request.user.is_professor() or quiz.created_by != request.user.professor:
        messages.error(request, "You are not authorized to delete this quiz.")
        return redirect('index')

    if request.method == "POST":  # Confirm deletion
        students_emails = CustomUser.objects.filter(
            student__group__in=quiz.groups.all(),  # Get students linked to the selected groups
            role="student",  # Ensure they are students
            ).values_list("email", flat=True)  # Extract only emails

            # Convert to a list (if needed)
        students_emails = list(students_emails)
        print("students_emails: ", students_emails)
            
        for student_email in students_emails:
            send_email_to_student_delete(request, student_email, quiz)
        quiz.delete()
        messages.success(request, "Quiz deleted successfully!")
        return redirect('professor')

    return render(request, 'quizes/edit_quiz.html', {'quiz': quiz})


@login_required
def create_project(request):

    if not request.user.is_professor():
        messages.error(request, "You are not authorized!.")
        return redirect('index')  
    professor = request.user.professor
    if request.method == 'POST':
        form = projectForm(request.POST, professor=professor)
        if form.is_valid():
            project = form.save(professor = professor)

            students_emails = list(CustomUser.objects.filter(
                student__group__in=project.groups.all(),
                role="student"
            ).values_list("email", flat=True))

            print("students_emails: ", students_emails)
            
            for student_email in students_emails:
                send_email_to_student_project(request, student_email, project)

            messages.success(request, "Project created successfully!")
            return redirect('index')  # Move redirect outside the loop

    else:
        form = projectForm(professor = professor)

    return render(request, 'projet/create_project.html', {'form': form})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(ProjectSubmissionTask, id=project_id)

    # Ensure only the professor who created the quiz can edit it
    if not request.user.is_professor():
        messages.error(request, "You are not authorized to edit this quiz.")
        print("hh")
        return redirect('index')  # Redirect unauthorized users
    
    if request.method == "POST":
        form = projectForm(request.POST, instance=project, professor=request.user.professor)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = projectForm(instance=project, professor=request.user.professor)
    return render(request, 'projet/edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(ProjectSubmissionTask, id=project_id)

    # Ensure only the professor who created the quiz can delete it
    if not request.user.is_professor():
        messages.error(request, "You are not authorized to delete this project.")
        return redirect('index')

    if request.method == "POST":  # Confirm deletion
        students_emails = CustomUser.objects.filter(
            student__group__in=project.groups.all(),  # Get students linked to the selected groups
            role="student",  # Ensure they are students
            ).values_list("email", flat=True)  # Extract only emails

            # Convert to a list (if needed)
        students_emails = list(students_emails)
        print("students_emails: ", students_emails)
            
        for student_email in students_emails:
            send_email_to_student_delete_project(request, student_email, project)
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect('professor')

    return render(request, 'projet/edit_project.html', {'project': project})


@login_required
def student_dashboard(request):
    # Ensure the user is a student
    if request.user.is_professor():
        messages.error(request, "You are not authorized!.")
        return redirect('index')

    student = Student.objects.get(user=request.user)
    current_time = now()

    # Fetch available project submission tasks assigned to the student's group
    available_projects = ProjectSubmissionTask.objects.filter(
        groups=student.group,
        start_time__lte=current_time,
        end_time__gte=current_time
    ).distinct()

    # Fetch available quizzes assigned to the student's group
    available_quizzes = Quiz.objects.filter(
        groups=student.group,
        start_time__lte=current_time,
        end_time__gte=current_time
    ).distinct()

    # Filter out quizzes where the student has already submitted results
    completed_quizzes = Result.objects.filter(student=student).values_list('quiz_id', flat=True)
    available_quizzes = available_quizzes.exclude(id__in=completed_quizzes)

    # Remove expired projects and quizzes
    available_projects = available_projects.exclude(end_time__lt=current_time)
    available_quizzes = available_quizzes.exclude(end_time__lt=current_time)

    context = {
        'student': student,
        'available_projects': available_projects,
        'available_quizzes': available_quizzes,
    }
    return render(request, 'pages/student_dashboard.html', context)
