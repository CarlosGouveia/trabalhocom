from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FormCadastroSevico, AtualizarServicoForm, DetalhaServicoForm
from django.contrib import messages
from .models import Service, CategoriaServico

@login_required
def myservices(request):
    servicos = Service.objects.filter(usuario_id=request.user)
    template_name = 'myservices.html'
    context = {'servicos': servicos}
    return render(request, template_name, context)

@login_required
def myservices_list_update(request):
    servicos = Service.objects.filter(usuario_id=request.user)
    template_name = 'myservices_list_update.html'
    context = {'servicos': servicos}
    return render(request, template_name, context)

@login_required
def detail_search(request, pk):
    servico = get_object_or_404(Service, pk=pk)
    context = {}
    if request.method == 'POST':
        form = DetalhaServicoForm(request.POST, instance=servico)
        if form.is_valid():
            servico = form.save(commit=False)
            servico.usuario = request.user
            servico.save()
            form = DetalhaServicoForm(instance=servico)
            context['success'] = True
            messages.success(request, 'Serviço selecionado!')
            return redirect('services:detail_search')
    else:
        form = AtualizarServicoForm(instance=servico)
    context['form'] = form
    template_name = 'detail_search.html'
    return render(request, template_name, context)

@login_required
def search_professionals(request):
    servicos = Service.objects.all()
    template_name = 'search_professionals.html'
    context = {'servicos': servicos}
    return render(request, template_name, context)

@login_required
def register_services(request):
    #popula_categoria()
    categoria = CategoriaServico.objects.all()
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

    context = {
        'form': form,
        'categoria': categoria,
    }
    return render(request, template_name, context)

def edit_services(request, pk):
    servico = get_object_or_404(Service, pk=pk)
    categoria = CategoriaServico.objects.all()
    context = {}
    if request.method == 'POST':
        form = AtualizarServicoForm(request.POST, instance=servico)
        if form.is_valid():
            servico = form.save(commit=False)
            servico.usuario = request.user
            servico.save()
            # form = AtualizarServicoForm(instance=servico)
            context['success'] = True
            messages.success(request, 'Serviço atualizado com sucesso!')
            return redirect('services:myservices_list_update')
    else:
        form = AtualizarServicoForm(instance=servico)
    context = {
        'form': form,
        'categoria': categoria,
    }
    template_name = 'edit_services.html'
    return render(request, template_name, context)


def popula_categoria():
    CategoriaServico.objects.create(nome='Agronomo')
    CategoriaServico.objects.create(nome='Ajudante de Pedreiro')
    CategoriaServico.objects.create(nome='Costureiro')
    CategoriaServico.objects.create(nome='Costureiro')
    CategoriaServico.objects.create(nome='Marceneiro')
    CategoriaServico.objects.create(nome='Pedreiro')
    CategoriaServico.objects.create(nome='Programador')
    CategoriaServico.objects.create(nome='Pedreiro')
    CategoriaServico.objects.create(nome='Marceneiro')
    CategoriaServico.objects.create(nome='Costureiro')
    CategoriaServico.objects.create(nome='Ajudante de Pedreiro')
    CategoriaServico.objects.create(nome='Agronomo')

