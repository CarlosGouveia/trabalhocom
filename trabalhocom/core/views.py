from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from trabalhocom.accounts.forms import login_form
from .forms import contato_form
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html', {'form_login': login_form, 'form_contato': contato_form})

def details(request):
    context = {}
    if request.method == 'POST':
        form = contato_form(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail()
            form = contato_form()
            messages.success(request, 'Mensagem enviada com sucesso')
            return redirect('/home/')
    else:
        form = contato_form()
    context['form'] = form
    template_name = 'home.html'
    return render(request, template_name, context)