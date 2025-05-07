from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from reportlab.pdfgen import canvas
from .models import *
from quizes.models import Quiz
from results.models import Result
from projetSubmission.models import ProjectSubmission
from projetTask.models import ProjectSubmissionTask
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import get_connection
from django.http import JsonResponse
import json
from questions.models import Question, Answer
from .models import Professor
from groupe.models import Group
from django.utils.timezone import now
from .forms import QuizForm, projectForm, meetingForm
from django.shortcuts import get_object_or_404
from datetime import datetime
from meetings.models import meeting

User = get_user_model()  # Get the CustomUser model

# Create your views here.

def index(request):
    if request.user.is_authenticated:  
        if request.user.is_professor:
            messages.success(request, "Welcome!")
            return redirect('professor')
        elif request.user.is_student:
            messages.success(request, "Welcome!")
            return redirect('student')
        else:
            messages.success(request, "Welcome!")
            return redirect('/admin/')

    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

    

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

def send_email_to_student_meeting(request, student_email, meet):
    try:
        user = User.objects.get(email=student_email)
        send_meeting_notification_email(request, user, student_email, meet)
    except User.DoesNotExist:
        messages.error(request, f"User with email {student_email} does not exist.")

def send_meeting_notification_email(request, user, to_email, meet):
    mail_subject = f"New Meeting Available: {meet.title}"
    message = render_to_string("pages/meetingNot.html", {
        'user': user,
        'meet': meet,
        'domain': get_current_site(request).domain,
        'protocol': 'http',  # Change to 'https' if using SSL
    })

    email = EmailMessage(mail_subject, message, to=[to_email], connection=get_connection())
    if email.send():
        messages.success(request, f'meeting notification sent to {user.first_name} {user.last_name}.')
    else:
        messages.error(request, f'Failed to send meeting notification to {user.first_name} {user.last_name}.')


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


def send_email_to_student_delete_meeting(request, student_email, meet):
    try:
        user = User.objects.get(email=student_email)
        send_quiz_notification_email_delete_meeting(request, user, student_email, meet)
    except User.DoesNotExist:
        messages.error(request, f"User with email {student_email} does not exist.")

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


def send_quiz_notification_email_delete_meeting(request, user, to_email, meet):
    mail_subject = f"meeting removed: {meet.title}"
    message = render_to_string("pages/meetingdelnot.html", {
        'user': user,
        'meet': meet,
        'domain': get_current_site(request).domain,
        'protocol': 'http',  # Change to 'https' if using SSL
    })

    email = EmailMessage(mail_subject, message, to=[to_email], connection=get_connection())
    if email.send():
        messages.success(request, f'meeting notification sent to {user.first_name} {user.last_name}.')
    else:
        messages.error(request, f'Failed to send meeting notification to {user.first_name} {user.last_name}.')



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


# def activateEmail(request, user, to_email):
#     mail_subject = "Activate your user account."
#     message = render_to_string("pages/user_email.html",{
#         'user':user,
#         'domain': get_current_site(request).domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user),
#         "protocol": 'http' 
#     })

#     email = EmailMessage(mail_subject, message, to=[to_email], connection=get_connection())
#     if email.send():
#         messages.success(request, f'{user}. SVP vérifier votre email : {to_email}.')
#     else:
#         messages.error(request, f'Something went wrong..., try verifying your email!') 


# def resend_verification(request):
#     email = request.session.get('pending_email')  # Get email from session

#     if not email:
#         messages.error(request, "Aucune adresse email trouvée. Inscrivez-vous d'abord.")
#         return redirect("registerPage")  # Redirect to registration if no email is found

#     try:
#         user = User.objects.get(email=email)
#         if user.is_active:
#             messages.info(request, "Ce compte est déjà activé.")
#         else:
#             activateEmail(request, user, user.email)
#             messages.success(request, "Un nouvel email de vérification a été envoyé !")
#     except User.DoesNotExist:
#         messages.error(request, "Aucun compte trouvé avec cet email.")

#     return render(request, "pages/verify_code.html", {"user_email": email})

def registerPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.is_active=False
            user.save() 
            # email = form.cleaned_data.get('email')
            # request.session['pending_email'] = email  # Store email in session
            # activateEmail(request, user, email)
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
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            if user.role == 'professor':  # Check the role directly on the CustomUser model
                login(request, user)
                return redirect('professor')
            elif user.role == 'student':  # Check the role directly on the CustomUser model
                login(request, user)
                return redirect('student')
            else:
                login(request, user)
                return redirect('/admin/')
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
    if request.user.is_student:
        messages.error(request, "You are not authorized to edit this quiz.")
        return redirect('index')
    professor = Professor.objects.get(user=request.user)
    groups = professor.groups.all()

    professor_quizzes = Quiz.objects.filter(created_by=professor)
    professor_projects = ProjectSubmissionTask.objects.filter(created_by=professor)
    professor_meeting = meeting.objects.filter(created_by=professor)

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
            project_scores = {}

            for project in projects:
                submission = ProjectSubmission.objects.filter(student=student, task=project).first()
    
                if submission:
                # Fetch the professor-assigned score, defaulting to 0 if not set
                    score = submission.grade if submission.grade is not None else 0
                    project_scores[project.id] = {
                    "score": score,
                    "file": submission.file.url if submission.file else None  # Include project file URL
                    }
                else:
                    project_scores[project.id] = {"score": 0, "file": None}  # No submission, default 0%       
                
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
        "professor_meetings": professor_meeting,
    }

    return render(request, "pages/professor_dashboard.html", context)

@login_required
def update_project_scores(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student_id = data.get("student_id")
        grades = data.get("grades", [])

        for grade in grades:
            project_id = grade["project_id"]
            score = int(grade["score"])

            submission = ProjectSubmission.objects.filter(student_id=student_id, task_id=project_id).first()
            if submission:
                submission.grade = score
                submission.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)

# def generate_student_pdf(request):
#     # Create the HttpResponse object with PDF content type
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="students_report.pdf"'

#     # Create PDF document
#     pdf = canvas.Canvas(response)
#     pdf.setFont("Helvetica", 14)
#     pdf.drawString(100, 800, "Students Dashboard Report")  # Title

#     # Fetch students from the database (modify as needed)
#     students = Student.objects.all()  # Adjust based on your model
#     y_position = 770  # Start position for student data

#     for student in students:
#         pdf.setFont("Helvetica", 12)
#         pdf.drawString(100, y_position, f"ID: {student.id}")
#         y_position -= 20  # Move down for the next student

#     pdf.showPage()
#     pdf.save()

#     return response


@login_required
def create_quiz(request):
    if not request.user.is_professor or not hasattr(request.user, 'professor'):
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

    if not request.user.is_professor or quiz.created_by != request.user.professor:
        messages.error(request, "You are not authorized to edit this quiz.")
        return redirect('index')

    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz, professor=request.user.professor)
        if form.is_valid():
            form.save()

            questions_texts = request.POST.getlist("questions[]")
            # CORRECTED: Retrieve correct answers by question index
            correct_answers = [
                request.POST.get(f"correct_answers[{i}]", 0)  # Default to 0 if missing
                for i in range(len(questions_texts))
            ]

            quiz.question_set.all().delete()

            for i, question_text in enumerate(questions_texts):
                if question_text.strip():
                    question = Question.objects.create(
                        quiz=quiz,
                        text=question_text,
                        created=datetime.now()
                    )

                    answers_texts = request.POST.getlist(f"answers[{i}][]")
                    # Parse the correct answer index for this question
                    correct_answer_index = int(correct_answers[i]) if i < len(correct_answers) else 0

                    for j, answer_text in enumerate(answers_texts):
                        if answer_text.strip():
                            Answer.objects.create(
                                question=question,
                                text=answer_text,
                                correct=(j == correct_answer_index),
                                created=datetime.now()
                            )
            print("Correct Answers:", correct_answers)  # After retrieving them

            messages.success(request, "Quiz updated successfully!")
            return redirect('professor')
    else:
        form = QuizForm(instance=quiz, professor=request.user.professor)

    return render(request, 'quizes/edit_quiz.html', {'form': form, 'quiz': quiz})
@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Ensure only the professor who created the quiz can delete it
    if not request.user.is_professor or quiz.created_by != request.user.professor:
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

    if not request.user.is_professor:
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
    if not request.user.is_professor:
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
    if not request.user.is_professor:
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
def create_meeting(request):
    if not request.user.is_professor:
        messages.error(request, "You are not authorized!.")
        return redirect('index')  
    professor = request.user.professor
    if request.method == 'POST':
        form = meetingForm(request.POST, professor=professor)
        if form.is_valid():
            meet = form.save(professor = professor)

            students_emails = list(CustomUser.objects.filter(
                student__group__in=meet.groups.all(),
                role="student"
            ).values_list("email", flat=True))

            print("students_emails: ", students_emails)
            
            for student_email in students_emails:
                send_email_to_student_project(request, student_email, meet)

            messages.success(request, "Meeting created successfully!")
            return redirect('index')  # Move redirect outside the loop

    else:
        form = meetingForm(professor = professor)

    return render(request, 'pages/create_meeting.html', {'form': form})   

@login_required
def edit_meeting(request, meeting_id):
    meet = get_object_or_404(meeting, id=meeting_id)

    # Ensure only the professor who created the quiz can edit it
    if not request.user.is_professor:
        messages.error(request, "You are not authorized to edit this quiz.")
        print("hh")
        return redirect('index')  # Redirect unauthorized users
    
    if request.method == "POST":
        form = meetingForm(request.POST, instance=meet, professor=request.user.professor)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = meetingForm(instance=meet, professor=request.user.professor)
    return render(request, 'pages/edit_meeting.html', {'form': form, 'meet': meet})

@login_required
def delete_meeting(request, meeting_id):
    meet = get_object_or_404(meeting, id=meeting_id)

    # Ensure only the professor who created the quiz can delete it
    if not request.user.is_professor:
        messages.error(request, "You are not authorized to delete this meeting.")
        return redirect('index')

    if request.method == "POST":  # Confirm deletion
        students_emails = CustomUser.objects.filter(
            student__group__in=meet.groups.all(),  # Get students linked to the selected groups
            role="student",  # Ensure they are students
            ).values_list("email", flat=True)  # Extract only emails

            # Convert to a list (if needed)
        students_emails = list(students_emails)
        print("students_emails: ", students_emails)
            
        for student_email in students_emails:
            send_email_to_student_delete_project(request, student_email, meet)
        meet.delete()
        messages.success(request, "meeting deleted successfully!")
        return redirect('professor')

    return render(request, 'projet/edit_project.html', {'project': meet})


@login_required
def student_dashboard(request):
    if request.user.is_professor:
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

    available_meetings = meeting.objects.filter(
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
    available_meetings = available_meetings.exclude(end_time__lt=current_time)
    # Fetch quiz results for notification
    quiz_results = Result.objects.filter(student=student)

    # Fetch graded project submissions for notification
    graded_projects = ProjectSubmission.objects.filter(student=student).exclude(grade=None)

    context = {
        'student': student,
        'available_projects': available_projects,
        'available_quizzes': available_quizzes,
        'available_meetings': available_meetings,
        'quiz_results': quiz_results,
        'graded_projects': graded_projects,
    }

    return render(request, 'pages/student_dashboard.html', context)

@login_required
def project_submission_view(request, task_id):
    student = get_object_or_404(Student, user=request.user)
    project_task = get_object_or_404(ProjectSubmissionTask, id=task_id)

    # Security checks
    if project_task.end_time < now():
        messages.error(request, "This project submission has expired.")
        return redirect("student")

    # if project_task.groups != student.group:
    #     messages.error(request, "You do not have permission to access this project.")
    #     return redirect("student")

    if request.method == "POST":
        file = request.FILES.get("file")
        

        # Prevent multiple submissions
        if ProjectSubmission.objects.filter(student=student, task=project_task).exists():
            project = ProjectSubmission.objects.get(student=student, task = project_task)
            project.delete()
            ProjectSubmission.objects.create(student=student, task=project_task, file=file)
            messages.success(request, "Project submitted successfully!")
            return redirect("student")

        else: 
            ProjectSubmission.objects.create(student=student, task=project_task, file=file)
            messages.success(request, "Project submitted successfully!")
            return redirect("student")

    return render(request, "projet/project_submission.html", {"project": project_task})



# # ✅ Step 1: Create Academic Session
# def add_academic_session(request):
#     if request.method == "POST":
#         form = AcademicSessionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('add_group')  # Redirect to Group Creation Page
#     else:
#         form = AcademicSessionForm()
    
#     return render(request, "admin/add_academic_session.html", {"form": form})

# # ✅ Step 2: Create Groups
# def add_group(request):
#     if request.method == "POST":
#         form = GroupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             if "add_another" in request.POST:
#                 return redirect('add_group')  # Stay on the same page to add more groups
#             return redirect('activate_users')  # Redirect to User Activation Page
#     else:
#         form = GroupForm()
    
#     return render(request, "admin/add_group.html", {"form": form})

# # ✅ Step 3: Activate Users
# def activate_users(request):
#     users = User.objects.all()
    
#     if request.method == "POST":
#         for user in users:
#             form = UserActivationForm(request.POST, instance=user)
#             if form.is_valid():
#                 form.save()
        
#         return redirect('index')  # Redirect to some admin home page

#     return render(request, "admin/activate_users.html", {"users": users})
