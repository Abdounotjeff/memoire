from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='registerPage'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logoutView'),
    path('verify/', views.verify_code, name='verify_code'),
    path("resend/", views.resend_verification_code, name="resend_verification"),
]