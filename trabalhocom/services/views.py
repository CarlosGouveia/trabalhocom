from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FormCadastroSevico, AtualizarServicoForm, DetalhaServicoForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from .models import Service, User
import json, os
from django.http import JsonResponse
from django.conf import settings
from .models import Service, CategoriaServico
from trabalhocom.services.forms import login_form
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

User = get_user_model()

def login_view_services(request):

    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('services:search-ALL-services')
        else:
            messages.error(request, 'Email ou senha incorretos!')
            return redirect('services:search-ALL-services')
    else:
        return redirect('services:search-ALL-services')

# LISTA TODOS OS SERVICOS DO USUARIO QUE ESTÁ LOGADO COM A OPÇÃO DE VER MAIS DETALHES
@login_required
def myservices(request):
    servicos = Service.objects.filter(usuario_id=request.user)
    template_name = 'myservices.html'
    context = {'servicos': servicos}
    return render(request, template_name, context)

# LISTA TODOS OS SERVICOS DO USUARIO QUE ESTÁ LOGADO COM A OPÇÃO DE EDITAR

# MOSTRA OS DETALHES DO SERVIÇO SELECIONADO
# @login_required
# def detail_search(request, pk):
#     servico = get_object_or_404(Service, pk=pk)
#     context = {}
#     if request.method == 'POST':
#         form = DetalhaServicoForm(request.POST, instance=servico)
#         if form.is_valid():
#             servico = form.save(commit=False)
#             servico.usuario = request.user
#             servico.save()
#             form = DetalhaServicoForm(instance=servico)
#             context['success'] = True
#             messages.success(request, 'Serviço selecionado!')
#             return redirect('services:detail_search')
#     else:
#         form = AtualizarServicoForm(instance=servico)
#     context['form'] = form
#     template_name = 'detail_search.html'
#     return render(request, template_name, context)

# LISTA TODOS OS SERVICOS DE TODOS OS USUARIOS
def search_All_services(request):
    categoria = CategoriaServico.objects.all()
    servicos = None

    if request.method == 'POST':
        descr = request.POST['descricao']
        categ = request.POST['categoria']
        est = request.POST['estado']
        cid = request.POST['cidade']

        # todos o campos
        if descr and categ and est and cid:
            servicos = Service.objects.filter(descricao_servico__icontains=descr).filter(categoria__nome=categ).filter(
                usuario__estado=est).filter(usuario__cidade=cid)

        # tres campos
        elif descr and categ and est and not cid:
            servicos = Service.objects.filter(descricao_servico__icontains=descr).filter(
                categoria__nome=categ).filter(usuario__estado=est)

        elif descr and categ and not est and cid:
            servicos = Service.objects.filter(descricao_servico__icontains=descr).filter(
                categoria__nome=categ).filter(usuario__cidade=cid)

        elif descr and not categ and est and cid:
            servicos = Service.objects.filter(descricao_servico__icontains=descr).filter(
                usuario__estado=est).filter(usuario__cidade=cid)

        elif not descr and categ and est and cid:
            servicos = Service.objects.filter(categoria__nome=categ).filter(
                usuario__estado=est).filter(usuario__cidade=cid)


        # dois campos
        elif descr and categ and not est and not cid:
            servicos = Service.objects.filter(descricao_servico__icontains=descr).filter(categoria__nome=categ)

        elif descr and not categ and est and not cid:
            servicos = Service.objects.filter(descricao_servico__icontains=descr).filter(usuario__estado=est)

        elif not descr and categ and est and not cid:
            servicos = Service.objects.filter(categoria__nome=categ).filter(usuario__estado=est)

        elif descr and not categ and not est and cid:
            servicos = Service.objects.filter(descricao_servico__icontains=descr).filter(usuario__cidade=cid)

        elif not descr and categ and not est and cid:
            servicos = Service.objects.filter(categoria__nome=categ).filter(usuario__cidade=cid)

        elif not descr and not categ and est and cid:
            servicos = Service.objects.filter(usuario__estado=est).filter(usuario__cidade=cid)


        #1 campo
        elif descr and not categ and not est and not cid:
            servicos = Service.objects.filter(descricao_servico__icontains=descr)

        elif not descr and categ and not est and not cid:
            servicos = Service.objects.filter(categoria__nome=categ)

        elif not descr and not categ and est and not cid:
            servicos = Service.objects.filter(usuario__estado=est)

        elif not descr and not categ and not est and cid:
            servicos = Service.objects.filter(usuario__cidade=cid)


        else:
            servicos = Service.objects.all()
    else:
        servicos = Service.objects.all()

    # PAGINAÇÃO
    paginator = Paginator(servicos, 1)
    page = request.GET.get('page')
    try:
        servicos = paginator.page(page)
    except PageNotAnInteger:
        servicos = paginator.page(1)
    except EmptyPage:
        servicos = paginator.page(paginator.num_pages)
    #FIM PAGINAÇÃO

    template_name = 'search_ALL_services.html'
    context = {
        'servicos': servicos,
        'estados': [],
        'categoria': categoria,
        'form_login': login_form
    }

    estado = json.loads(open(os.path.join(settings.BASE_DIR, 'trabalhocom/accounts/estado-cidade.json')).read())

    for i in range(len(estado)):
        context['estados'].append({'nome': estado[i]['nome'], 'uf': estado[i]['sigla']})

    return render(request, template_name, context)

# REGISTRO DE SERVIÇOS
@login_required
def register_services(request):
    # popula_categoria()
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

@login_required
def mais_detalhes(request, pk):
    print('entrou tbm')
    servico = Service.objects.filter(pk=pk)

    context = {
        'servico': servico
    }
    template_name = 'mais_detalhes.html'
    return render(request, template_name, context)

@login_required
def myservices_details(request, pk):
    servico = Service.objects.filter(pk=pk)

    context = {
        'servico': servico
    }

    template_name = 'myservices_details.html'
    return render(request, template_name, context)

# EDITAR SERVIÇOS
def edit_services(request, pk):
    # print('ENTRO AKI CARAI')
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
            return redirect('services:myservices')
    else:
        form = AtualizarServicoForm(instance=servico)
    context = {
        'form': form,
        'categoria': categoria,
    }
    template_name = 'edit_services.html'
    return render(request, template_name, context)


def get_cidades(request, uf):
    data = json.loads(open(os.path.join(settings.BASE_DIR, 'trabalhocom/accounts/estado-cidade.json')).read())

    context = {
        'cidades': []
    }

    for i in range(len(data)):
        if data[i]['sigla'] == uf:
            cidades = data[i]['cidades']

    context['cidades'].append('<option value="" selected>Selecione uma cidade...</option>')
    for cidade in cidades:
        context['cidades'].append("<option value='"+cidade+"'>"+cidade+"</option>")

    return JsonResponse(context)

@login_required
def service_remove(request, pk):
    servico = get_object_or_404(Service, pk=pk)
    servico.delete()
    return redirect('services:myservices')


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

