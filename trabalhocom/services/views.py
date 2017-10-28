from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def myservices(request):
    template_name = 'myservices.html'
    return render(request, template_name)

@login_required
def register_services(request):
    template_name = 'register_services.html'
    return render(request, template_name)

@login_required
def search_professionals(request):
    template_name = 'search_professionals.html'
    return render(request, template_name)
