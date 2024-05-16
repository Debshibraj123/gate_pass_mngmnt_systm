# security/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from .forms import GatePassForm


def security_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('security_login')
    else:
        form = UserCreationForm()
    return render(request, 'security/register.html', {'form': form})

def security_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to a new page after login
            return render(request, 'security/security_dashboard.html')
    else:
        form = AuthenticationForm()
    return render(request, 'security/login.html', {'form': form})



def officer_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return render(request, 'officers/off_dashboard.html')  # Redirect to officer dashboard after registration
    else:
        form = UserCreationForm()
    return render(request, 'officers/off_register.html', {'form': form})

def officer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'officers/off_dashboard.html')
    else:
        form = AuthenticationForm()
    return render(request, 'officers/off_login.html', {'form': form})


def home(request):
    return render(request, 'homepage.html')


def officer_dashboard(request):
    if request.method == 'POST':
        form = GatePassForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('officer_dashboard')  # Redirect to dashboard after successfully creating gate pass
    else:
        form = GatePassForm()
    return render(request, 'officers/off_dashboard.html', {'form': form})