from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='registerPage'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logoutView'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]