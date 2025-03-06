from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode

from documents.tokens import account_activation_token  # Ensure this exists
from .models import Student, Professor  # Import other models if needed

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'is_superuser', 'send_activation_email')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Role & Status', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Permissions', {'fields': ('user_permissions', 'groups')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )

    def send_activation_email(self, obj):
        """ Creates a button for sending an activation email """
        if not obj.is_active:  # Show button only for inactive users
            url = reverse('admin:send_activation_email', args=[obj.id])
            return format_html('<a class="button" href="{}" style="background: #007bff; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Send Activation Email</a>', url)
        return "Already Activated"  # Display text if user is already active

    send_activation_email.short_description = "Activation Email"

    def get_urls(self):
        """ Adds a custom admin URL to handle activation email sending """
        urls = super().get_urls()
        custom_urls = [
            path('send-activation-email/<int:user_id>/', self.admin_site.admin_view(self.send_activation_email_view), name='send_activation_email'),
        ]
        return custom_urls + urls

    def send_activation_email_view(self, request, user_id):
        """ Handles sending activation email when the button is clicked """
        user = User.objects.get(pk=user_id)

        if user.is_active:
            messages.warning(request, "User is already activated.")
            return redirect(reverse('admin:documents_customuser_changelist'))  # Dynamically redirect to the user list

        # Call activateEmail function to send activation email
        try:
            mail_subject = "Activate your user account."
            message = render_to_string("pages/user_email.html", {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                "protocol": 'http'
            })

            email = EmailMessage(mail_subject, message, to=[user.email], connection=get_connection())
            email.send()

            messages.success(request, f"Activation email sent successfully to {user.email}")
        except Exception as e:
            messages.error(request, f"Error sending email: {str(e)}")

        return redirect(reverse('admin:documents_customuser_changelist'))  # Redirect back to the users list

# Professor Admin
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    filter_horizontal = ('groups',)  # To select multiple groups in the admin panel


# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Professor, ProfessorAdmin)
