# security/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.security_register, name='security_register'),
    path('login/', views.security_login, name='security_login'),
    path('off_register/', views.officer_register, name='officer_register'),
    path('off_login/', views.officer_login, name='officer_login'),
    path('off_dashboard/', views.officer_dashboard, name='officer_dashboard'),
]
