from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='registerPage'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logoutView'),
    path('resend/', views.resend_verification, name ='resend_verification'),
    path('verify/', views.activ, name='activ'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('Quiz/', views.Quiz, name='Quiz'),
    path('professor/', views.professor_dashboard, name='professor'),
    path('create-quiz/', views.create_quiz, name='create_quiz'),
    path('edit-quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('delete-quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('create-project/', views.create_project, name='create_project'),
    path('edit-project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    
]