from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from .forms import RegisterForm, EditAccountForm, PasswordResetForm, AlteraSenha, EditarSenha
from .models import PasswordReset
import json

User = get_user_model()

def login_view(request):

    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Email ou senha incorretos!')
            return redirect('/')
    else:
        return redirect('/')

    return render(request, 'home.html')


def password_reset(request):
    template_name = 'accounts/password_reset.html'
    context = {}
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
        context['sucess'] = True
    context['form'] = form
    return render(request, template_name, context)

def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = AlteraSenha(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['sucess'] = True
    context['form'] = form
    return render(request, template_name, context)


@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    return render(request, template_name)

@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance=request.user)
            context['success'] = True
            messages.success(request, 'Cadastro atualizado com sucesso!')
            return redirect('accounts:edit')
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)

def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(email=user.email, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('core:home')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)

@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = EditarSenha(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['sucess'] = True
    else:
        form = EditarSenha(user=request.user)
    context['form'] = form
    return render(request, template_name, context)
