from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FormCadastroSevico, AtualizarServicoForm
from django.contrib import messages
from .models import Service

@login_required
def myservices(request):
    servicos = Service.objects.all()
    template_name = 'myservices.html'
    context = {'servicos': servicos}
    return render(request, template_name, context)

@login_required
def myservices_list_update(request):
    servicos = Service.objects.all()
    template_name = 'myservices_list_update.html'
    context = {'servicos': servicos}
    return render(request, template_name, context)

@login_required
def search_professionals(request):
    template_name = 'search_professionals.html'
    return render(request, template_name)

@login_required
def register_services(request):
    template_name = 'register_services.html'
    context = {}
    if request.method == 'POST':
        form = FormCadastroSevico(request.POST)
        if form.is_valid():
            form.save(request)
            context['success'] = True
            messages.success(request, 'Serviço cadastrado com sucesso!')
            return redirect('services:register_services')
    else:
        form = FormCadastroSevico()

    context['form'] = form
    return render(request, template_name, context)

def edit_services(request):

    template_name = 'edit_services.html'
    context = {}
    if request.method == 'POST':
        form = AtualizarServicoForm(request.POST, instance=request.user)
        print(form)
        if form.is_valid():
            form.save()
            form = AtualizarServicoForm(instance=request.user)
            context['success'] = True
            messages.success(request, 'Servico atualizado com sucesso!')
            return redirect('services:edit_services')
    else:
        form = AtualizarServicoForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)
