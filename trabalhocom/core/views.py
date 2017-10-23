from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from trabalhocom.accounts.forms import login_form

# Create your views here.

def home(request):
    return render(request, 'home.html', {'form': login_form})