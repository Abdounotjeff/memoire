from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import *
from .models import EmailVerification
import secrets
from django.core.mail import send_mail

# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def send_verification_email(user):
    code = secrets.token_hex(3)  # Generate a random code
    EmailVerification.objects.create(user=user, code=code)  # Save in DB

    subject = "Verify Your Email"
    message = f"Hello {user.username},\n\nYour verification code is: {code}\n\nEnter this code to verify your identity."
    from_email = "your_email@gmail.com"
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


User = get_user_model()  # Get the CustomUser model

def registerPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # This already creates the user
            
            # Create an EmailVerification entry
            verification_code = secrets.token_hex(3)  # Generate a random 6-character hex code
            EmailVerification.objects.create(user=user, code=verification_code)
            
            # Send the verification email
            send_verification_email(user)

            # Success message
            messages.success(request, f'Account was created for {user.username}. Please verify your email.')
            return redirect('loginPage')
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
            return redirect('profile')
        else:
            messages.info(request, 'Username OR password is incorrect')
    return render(request, 'pages/login.html', context={})


@login_required
def logoutUser(request):
    logout(request)
    return redirect('loginPage')


def verify_code(request):
    if request.method == "POST":
        entered_code = request.POST["code"]
        verification = EmailVerification.objects.get(user=request.user)

        if verification.code == entered_code:
            verification.verified = True
            verification.save()
            return HttpResponse("Verification successful!")
        else:
            return HttpResponse("Invalid code. Please try again.")

    return render(request, "pages/verify_code.html")

@login_required
def resend_verification_code(request):
    user = request.user

    try:
        verification = EmailVerification.objects.get(user=user)
        new_code = secrets.token_hex(3)  # Generate a new 6-character code
        verification.code = new_code  # Update the code in DB
        verification.save()

        # Send the new verification email
        send_mail(
            "Resend: Verify Your Email",
            f"Hello {user.username},\n\nYour new verification code is: {new_code}",
            "your_email@gmail.com",
            [user.email],
        )
    except EmailVerification.DoesNotExist:
        pass  # Handle case where user has no verification entry

    return redirect("pages/verify_code")  # Redirect back to verification page