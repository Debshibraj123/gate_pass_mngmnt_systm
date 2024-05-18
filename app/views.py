# security/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from .forms import GatePassForm
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import GatePass
from .forms import OnSpotRegistrationForm
from django.conf import settings


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

def security_dashboard(request):
    gate_passes = GatePass.objects.all()
    return render(request, 'security/security_dashboard.html', {'gate_passes': gate_passes})


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
    gate_passes = GatePass.objects.all()
    if request.method == 'POST':
        form = GatePassForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gate pass request submitted successfully')

            # Clear the form data after successful submission
            form = GatePassForm()  # Create a new, empty form instance

            return render(request, 'homepage.html', {'form': form, 'gate_passes': gate_passes})
    else:
        form = GatePassForm()
    return render(request, 'officers/off_dashboard.html', {'form': form, 'gate_passes': gate_passes})


#print the pdf

def generate_pdf(request, gate_pass_id):
    gate_pass = GatePass.objects.get(pk=gate_pass_id)

    template_path = 'officers/gate_pass_template.html'
    context = {'gate_pass': gate_pass}
    
    # Render the HTML template
    template = get_template(template_path)
    html = template.render(context)
    
    # Create a PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="gate_pass_{gate_pass.name}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error rendering PDF', status=500)
    
    return response




def on_spot_registration(request):
    if request.method == 'POST':
        form = OnSpotRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('security_dashboard')
    else:
        form = OnSpotRegistrationForm()
    return render(request, 'security/on_spot_registration.html', {'form': form})


def generate_pdf_sec(request, gate_pass_id):
    gate_pass = get_object_or_404(GatePass, id=gate_pass_id)
    template_path = 'security/gate_pass_template.html'
    context = {'gate_pass': gate_pass}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="gate_pass_{gate_pass_id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse('We had some errors with code %s' % pisa_status.err, status=400)
    return response

import os
def link_callback(uri, rel):
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path