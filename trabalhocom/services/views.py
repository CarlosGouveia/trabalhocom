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

@login_required
def mais_detalhes(request, pk):
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
    CategoriaServico.objects.create(nome='Abastecedor')
    CategoriaServico.objects.create(nome='Acabador de Embalagens')
    CategoriaServico.objects.create(nome='Açougueiro')
    CategoriaServico.objects.create(nome='Acrilista')
    CategoriaServico.objects.create(nome='Acupunturista')
    CategoriaServico.objects.create(nome='Aderecista')
    CategoriaServico.objects.create(nome='Adesivador')
    CategoriaServico.objects.create(nome='Adestrador')
    CategoriaServico.objects.create(nome='Administrador')
    CategoriaServico.objects.create(nome='Advogado')
    CategoriaServico.objects.create(nome='Afiador de Ferramentas')
    CategoriaServico.objects.create(nome='Agente de Aeroporto')
    CategoriaServico.objects.create(nome='Agente de Segurança')
    CategoriaServico.objects.create(nome='Agente de Serviços')
    CategoriaServico.objects.create(nome='Agente de Viagens')
    CategoriaServico.objects.create(nome='Agente Funerário')
    CategoriaServico.objects.create(nome='Ajudante')
    CategoriaServico.objects.create(nome='Alfaiate')
    CategoriaServico.objects.create(nome='Alinhador')
    CategoriaServico.objects.create(nome='Almoxarife')
    CategoriaServico.objects.create(nome='Alpinista Industrial')
    CategoriaServico.objects.create(nome='Amarrador')
    CategoriaServico.objects.create(nome='Analista')
    CategoriaServico.objects.create(nome='Animador de Festas')
    CategoriaServico.objects.create(nome='Animador Digital')
    CategoriaServico.objects.create(nome='Antropólogo')
    CategoriaServico.objects.create(nome='Apontador de Obras')
    CategoriaServico.objects.create(nome='Apontador de Produção')
    CategoriaServico.objects.create(nome='Aprendiz')
    CategoriaServico.objects.create(nome='Apresentador de Programa de Televisão')
    CategoriaServico.objects.create(nome='Aquarista')
    CategoriaServico.objects.create(nome='Armador')
    CategoriaServico.objects.create(nome='Armazenista')
    CategoriaServico.objects.create(nome='Arqueólogo')
    CategoriaServico.objects.create(nome='Arquiteto')
    CategoriaServico.objects.create(nome='Arquivista')
    CategoriaServico.objects.create(nome='Arrematador')
    CategoriaServico.objects.create(nome='Arte-finalista')
    CategoriaServico.objects.create(nome='Artesão')
    CategoriaServico.objects.create(nome='Articulador Social')
    CategoriaServico.objects.create(nome='Ascensorista')
    CategoriaServico.objects.create(nome='Assessor')
    CategoriaServico.objects.create(nome='Assistente')
    CategoriaServico.objects.create(nome='Assoalhador')
    CategoriaServico.objects.create(nome='Atendente')
    CategoriaServico.objects.create(nome='Atendimento Publicitário')
    CategoriaServico.objects.create(nome='Ator')
    CategoriaServico.objects.create(nome='Atuário')
    CategoriaServico.objects.create(nome='Auditor')
    CategoriaServico.objects.create(nome='Auxiliar')
    CategoriaServico.objects.create(nome='Avaliador de Imóveis')
    CategoriaServico.objects.create(nome='Avaliador de Veículos')
    CategoriaServico.objects.create(nome='Avaliador Físico')
    CategoriaServico.objects.create(nome='Azulejista')
    CategoriaServico.objects.create(nome='Babá')
    CategoriaServico.objects.create(nome='Back Office')
    CategoriaServico.objects.create(nome='Balanceiro')
    CategoriaServico.objects.create(nome='Balconista')
    CategoriaServico.objects.create(nome='Bamburista')
    CategoriaServico.objects.create(nome='Barista')
    CategoriaServico.objects.create(nome='Barman')
    CategoriaServico.objects.create(nome='Berçarista')
    CategoriaServico.objects.create(nome='Bibliotecário')
    CategoriaServico.objects.create(nome='Bilheteiro')
    CategoriaServico.objects.create(nome='Biologista')
    CategoriaServico.objects.create(nome='Biólogo')
    CategoriaServico.objects.create(nome='Biomédico')
    CategoriaServico.objects.create(nome='Bioquímico')
    CategoriaServico.objects.create(nome='Biotecnólogo')
    CategoriaServico.objects.create(nome='Blaster')
    CategoriaServico.objects.create(nome='Blogueiro')
    CategoriaServico.objects.create(nome='Bloquista')
    CategoriaServico.objects.create(nome='Bombeiro Civil')
    CategoriaServico.objects.create(nome='Bombeiro Industrial')
    CategoriaServico.objects.create(nome='Booker')
    CategoriaServico.objects.create(nome='Bordador')
    CategoriaServico.objects.create(nome='Borracheiro')
    CategoriaServico.objects.create(nome='Business Partner')
    CategoriaServico.objects.create(nome='Cabeleireiro')
    CategoriaServico.objects.create(nome='Cabista')
    CategoriaServico.objects.create(nome='Caixa de Banco')
    CategoriaServico.objects.create(nome='Calceteiro')
    CategoriaServico.objects.create(nome='Calculista')
    CategoriaServico.objects.create(nome='Caldeireiro')
    CategoriaServico.objects.create(nome='Camareiro')
    CategoriaServico.objects.create(nome='Caracterizador')
    CategoriaServico.objects.create(nome='Carpinteiro')
    CategoriaServico.objects.create(nome='Cartazista')
    CategoriaServico.objects.create(nome='Carteiro')
    CategoriaServico.objects.create(nome='Caseiro')
    CategoriaServico.objects.create(nome='Cenógrafo')
    CategoriaServico.objects.create(nome='Cenotécnico')
    CategoriaServico.objects.create(nome='Chapeiro')
    CategoriaServico.objects.create(nome='Chaveiro')
    CategoriaServico.objects.create(nome='Churrasqueiro')
    CategoriaServico.objects.create(nome='Cilindrista')
    CategoriaServico.objects.create(nome='Cinegrafista')
    CategoriaServico.objects.create(nome='Classificador de Grãos')
    CategoriaServico.objects.create(nome='Cliente Oculto')
    CategoriaServico.objects.create(nome='Coach')
    CategoriaServico.objects.create(nome='Cobrador de Ônibus')
    CategoriaServico.objects.create(nome='Codificador de Dados')
    CategoriaServico.objects.create(nome='Colchoeiro')
    CategoriaServico.objects.create(nome='Coletor de Amostras')
    CategoriaServico.objects.create(nome='Coletor de Lixo')
    CategoriaServico.objects.create(nome='Colocador de Papel de Parede')
    CategoriaServico.objects.create(nome='Colorista')
    CategoriaServico.objects.create(nome='Comissário de Avarias')
    CategoriaServico.objects.create(nome='Comissário de Bordo')
    CategoriaServico.objects.create(nome='Comprador')
    CategoriaServico.objects.create(nome='Comunicador Social')
    CategoriaServico.objects.create(nome='Concierge')
    CategoriaServico.objects.create(nome='Confeiteiro')
    CategoriaServico.objects.create(nome='Conferente')
    CategoriaServico.objects.create(nome='Conselheiro Tutelar')
    CategoriaServico.objects.create(nome='Consultor')
    CategoriaServico.objects.create(nome='Contabilista')
    CategoriaServico.objects.create(nome='Contador')
    CategoriaServico.objects.create(nome='Contador Gerencial')
    CategoriaServico.objects.create(nome='Contato Publicitário')
    CategoriaServico.objects.create(nome='Conteudista')
    CategoriaServico.objects.create(nome='Contínuo')
    CategoriaServico.objects.create(nome='Contra-regra')
    CategoriaServico.objects.create(nome='Controlador')
    CategoriaServico.objects.create(nome='Controller')
    CategoriaServico.objects.create(nome='Coordenador')
    CategoriaServico.objects.create(nome='Copeiro')
    CategoriaServico.objects.create(nome='Copiador de Chapa')
    CategoriaServico.objects.create(nome='Coreógrafo')
    CategoriaServico.objects.create(nome='Corretor de Imóveis')
    CategoriaServico.objects.create(nome='Corretor de Seguros')
    CategoriaServico.objects.create(nome='Cortador')
    CategoriaServico.objects.create(nome='Costureiro')
    CategoriaServico.objects.create(nome='Cozinheiro')
    CategoriaServico.objects.create(nome='Crepeiro')
    CategoriaServico.objects.create(nome='Cronoanalista')
    CategoriaServico.objects.create(nome='Cuidador')
    CategoriaServico.objects.create(nome='Cumim')
    CategoriaServico.objects.create(nome='Curador de Arte')
    CategoriaServico.objects.create(nome='Dançarino')
    CategoriaServico.objects.create(nome='Data Scientist')
    CategoriaServico.objects.create(nome='DBA')
    CategoriaServico.objects.create(nome='Decorador')
    CategoriaServico.objects.create(nome='Dedetizador')
    CategoriaServico.objects.create(nome='Degustador')
    CategoriaServico.objects.create(nome='Dentista')
    CategoriaServico.objects.create(nome='Depiladora')
    CategoriaServico.objects.create(nome='Dermoconsultor')
    CategoriaServico.objects.create(nome='Desenhista')
    CategoriaServico.objects.create(nome='Desentupidor')
    CategoriaServico.objects.create(nome='Designer')
    CategoriaServico.objects.create(nome='Despachante')
    CategoriaServico.objects.create(nome='Diagramador')
    CategoriaServico.objects.create(nome='Digitador')
    CategoriaServico.objects.create(nome='Digitalizador')
    CategoriaServico.objects.create(nome='Diligenciador')
    CategoriaServico.objects.create(nome='Diretor')
    CategoriaServico.objects.create(nome='Divulgador')
    CategoriaServico.objects.create(nome='DJ')
    CategoriaServico.objects.create(nome='Documentador')
    CategoriaServico.objects.create(nome='Doméstica')
    CategoriaServico.objects.create(nome='Duteiro')
    CategoriaServico.objects.create(nome='Ecólogo')
    CategoriaServico.objects.create(nome='Economista')
    CategoriaServico.objects.create(nome='Editor de Imagens')
    CategoriaServico.objects.create(nome='Editor de Moda')
    CategoriaServico.objects.create(nome='Editor de Texto')
    CategoriaServico.objects.create(nome='Editor de Vídeo')
    CategoriaServico.objects.create(nome='Educador Ambiental')
    CategoriaServico.objects.create(nome='Educador Social')
    CategoriaServico.objects.create(nome='Eletricista')
    CategoriaServico.objects.create(nome='Eletromecânico')
    CategoriaServico.objects.create(nome='Eletrotécnico')
    CategoriaServico.objects.create(nome='Embalador')
    CategoriaServico.objects.create(nome='Embriologista')
    CategoriaServico.objects.create(nome='Emissor de CTRC')
    CategoriaServico.objects.create(nome='Emissor de Passagens')
    CategoriaServico.objects.create(nome='Empacotador')
    CategoriaServico.objects.create(nome='Encadernador')
    CategoriaServico.objects.create(nome='Encanador')
    CategoriaServico.objects.create(nome='Encapsulador')
    CategoriaServico.objects.create(nome='Enfermeiro')
    CategoriaServico.objects.create(nome='Enfestador')
    CategoriaServico.objects.create(nome='Engenheiro')
    CategoriaServico.objects.create(nome='Entregador')
    CategoriaServico.objects.create(nome='Ergonomista')
    CategoriaServico.objects.create(nome='Escrevente')
    CategoriaServico.objects.create(nome='Escriturário')
    CategoriaServico.objects.create(nome='Estampador')
    CategoriaServico.objects.create(nome='Estatístico')
    CategoriaServico.objects.create(nome='Esteticista')
    CategoriaServico.objects.create(nome='Estilista')
    CategoriaServico.objects.create(nome='Estofador')
    CategoriaServico.objects.create(nome='Estoquista')
    CategoriaServico.objects.create(nome='Etiquetador')
    CategoriaServico.objects.create(nome='Executivo de Contas')
    CategoriaServico.objects.create(nome='Executivo de Vendas')
    CategoriaServico.objects.create(nome='Extrusor')
    CategoriaServico.objects.create(nome='Farmacêutico')
    CategoriaServico.objects.create(nome='Faturista')
    CategoriaServico.objects.create(nome='Faturista Hospitalar')
    CategoriaServico.objects.create(nome='Ferramenteiro')
    CategoriaServico.objects.create(nome='Ferreiro')
    CategoriaServico.objects.create(nome='Figurinista')
    CategoriaServico.objects.create(nome='Fiscal de Caixa')
    CategoriaServico.objects.create(nome='Fiscal de Campo')
    CategoriaServico.objects.create(nome='Fiscal de Loja')
    CategoriaServico.objects.create(nome='Fiscal de Obras')
    CategoriaServico.objects.create(nome='Fiscal de Prevenção de Perdas')
    CategoriaServico.objects.create(nome='Fiscal de Tráfego')
    CategoriaServico.objects.create(nome='Físico')
    CategoriaServico.objects.create(nome='Fisioterapeuta')
    CategoriaServico.objects.create(nome='Florista')
    CategoriaServico.objects.create(nome='Fonoaudiólogo')
    CategoriaServico.objects.create(nome='Forneiro')
    CategoriaServico.objects.create(nome='Fotógrafo')
    CategoriaServico.objects.create(nome='Fotogravador')
    CategoriaServico.objects.create(nome='Fracionador')
    CategoriaServico.objects.create(nome='Frentista')
    CategoriaServico.objects.create(nome='Fresador')
    CategoriaServico.objects.create(nome='Fresador CNC')
    CategoriaServico.objects.create(nome='Fundidor de Metais')
    CategoriaServico.objects.create(nome='Funileiro')
    CategoriaServico.objects.create(nome='Funileiro de Veículos')
    CategoriaServico.objects.create(nome='Galvanizador')
    CategoriaServico.objects.create(nome='Garantista')
    CategoriaServico.objects.create(nome='Garantista de Veículos')
    CategoriaServico.objects.create(nome='Garçom')
    CategoriaServico.objects.create(nome='Garde Manger')
    CategoriaServico.objects.create(nome='Gastrônomo')
    CategoriaServico.objects.create(nome='Gemólogo')
    CategoriaServico.objects.create(nome='Geofísico')
    CategoriaServico.objects.create(nome='Geógrafo')
    CategoriaServico.objects.create(nome='Geólogo')
    CategoriaServico.objects.create(nome='Gerente')
    CategoriaServico.objects.create(nome='Gerontólogo')
    CategoriaServico.objects.create(nome='Gesseiro')
    CategoriaServico.objects.create(nome='Gestor Ambiental')
    CategoriaServico.objects.create(nome='Gestor Portuário')
    CategoriaServico.objects.create(nome='Governanta')
    CategoriaServico.objects.create(nome='Greidista')
    CategoriaServico.objects.create(nome='Guia de Turismo')
    CategoriaServico.objects.create(nome='Historiador')
    CategoriaServico.objects.create(nome='Hostess')
    CategoriaServico.objects.create(nome='Ilustrador')
    CategoriaServico.objects.create(nome='Impermeabilizador')
    CategoriaServico.objects.create(nome='Implantador de Sistemas')
    CategoriaServico.objects.create(nome='Impressor')
    CategoriaServico.objects.create(nome='Inspetor')
    CategoriaServico.objects.create(nome='Instalador')
    CategoriaServico.objects.create(nome='Instrumentador Cirúrgico')
    CategoriaServico.objects.create(nome='Instrumentista')
    CategoriaServico.objects.create(nome='Instrutor')
    CategoriaServico.objects.create(nome='Intérprete')
    CategoriaServico.objects.create(nome='Intérprete de Libras')
    CategoriaServico.objects.create(nome='Jardineiro')
    CategoriaServico.objects.create(nome='Jatista')
    CategoriaServico.objects.create(nome='Jornaleiro')
    CategoriaServico.objects.create(nome='Jornalista')
    CategoriaServico.objects.create(nome='Laboratorista de Concreto')
    CategoriaServico.objects.create(nome='Laboratorista de Solos')
    CategoriaServico.objects.create(nome='Laboratorista Fotográfico')
    CategoriaServico.objects.create(nome='Lactarista')
    CategoriaServico.objects.create(nome='Laminador')
    CategoriaServico.objects.create(nome='Lancheiro')
    CategoriaServico.objects.create(nome='Lapidador de Gemas')
    CategoriaServico.objects.create(nome='Lapidador de Vidros')
    CategoriaServico.objects.create(nome='Laqueador')
    CategoriaServico.objects.create(nome='Lavadeiro')
    CategoriaServico.objects.create(nome='Lavador')
    CategoriaServico.objects.create(nome='Lavador de Veículos')
    CategoriaServico.objects.create(nome='Layoutista')
    CategoriaServico.objects.create(nome='Leiturista')
    CategoriaServico.objects.create(nome='Letrista')
    CategoriaServico.objects.create(nome='Limpador')
    CategoriaServico.objects.create(nome='Limpador de Vidros')
    CategoriaServico.objects.create(nome='Lingotador')
    CategoriaServico.objects.create(nome='Lixador')
    CategoriaServico.objects.create(nome='Locutor')
    CategoriaServico.objects.create(nome='Lubrificador')
    CategoriaServico.objects.create(nome='Lustrador de Móveis')
    CategoriaServico.objects.create(nome='Maçariqueiro')
    CategoriaServico.objects.create(nome='Mãe Social')
    CategoriaServico.objects.create(nome='Magarefe')
    CategoriaServico.objects.create(nome='Maître')
    CategoriaServico.objects.create(nome='Mandrilhador')
    CategoriaServico.objects.create(nome='Manicure e Pedicure')
    CategoriaServico.objects.create(nome='Manipulador de Cosméticos')
    CategoriaServico.objects.create(nome='Manipulador de Farmácia')
    CategoriaServico.objects.create(nome='Manobrista')
    CategoriaServico.objects.create(nome='Maqueiro')
    CategoriaServico.objects.create(nome='Maquetista')
    CategoriaServico.objects.create(nome='Maquiador')
    CategoriaServico.objects.create(nome='Maquinista de Trem')
    CategoriaServico.objects.create(nome='Marceneiro')
    CategoriaServico.objects.create(nome='Marinheiro')
    CategoriaServico.objects.create(nome='Marmorista')
    CategoriaServico.objects.create(nome='Marteleteiro')
    CategoriaServico.objects.create(nome='Masseiro')
    CategoriaServico.objects.create(nome='Massoterapeuta')
    CategoriaServico.objects.create(nome='Matemático')
    CategoriaServico.objects.create(nome='Mecânico')
    CategoriaServico.objects.create(nome='Médico')
    CategoriaServico.objects.create(nome='Medidor de Obras')
    CategoriaServico.objects.create(nome='Meio Oficial')
    CategoriaServico.objects.create(nome='Mensageiro')
    CategoriaServico.objects.create(nome='Mensageiro de Hotel')
    CategoriaServico.objects.create(nome='Merendeira')
    CategoriaServico.objects.create(nome='Mestre Cervejeiro')
    CategoriaServico.objects.create(nome='Mestre de Cabotagem')
    CategoriaServico.objects.create(nome='Mestre de Obras')
    CategoriaServico.objects.create(nome='Meteorologista')
    CategoriaServico.objects.create(nome='Metrologista')
    CategoriaServico.objects.create(nome='Microbiologista')
    CategoriaServico.objects.create(nome='Modelista')
    CategoriaServico.objects.create(nome='Modelo')
    CategoriaServico.objects.create(nome='Moldador')
    CategoriaServico.objects.create(nome='Moldureiro')
    CategoriaServico.objects.create(nome='Moleiro')
    CategoriaServico.objects.create(nome='Monitor')
    CategoriaServico.objects.create(nome='Montador')
    CategoriaServico.objects.create(nome='Mordomo')
    CategoriaServico.objects.create(nome='Motoboy')
    CategoriaServico.objects.create(nome='Motorista')
    CategoriaServico.objects.create(nome='Museólogo')
    CategoriaServico.objects.create(nome='Músico')
    CategoriaServico.objects.create(nome='Musicoterapeuta')
    CategoriaServico.objects.create(nome='Naturólogo')
    CategoriaServico.objects.create(nome='Neuropsicólogo')
    CategoriaServico.objects.create(nome='Nivelador')
    CategoriaServico.objects.create(nome='Nutricionista')
    CategoriaServico.objects.create(nome='Oceanógrafo')
    CategoriaServico.objects.create(nome='Office-boy')
    CategoriaServico.objects.create(nome='Oficial')
    CategoriaServico.objects.create(nome='Operador')
    CategoriaServico.objects.create(nome='Orçamentista')
    CategoriaServico.objects.create(nome='Orçamentista Civil')
    CategoriaServico.objects.create(nome='Orientador Educacional')
    CategoriaServico.objects.create(nome='Orientador Sócio Educativo')
    CategoriaServico.objects.create(nome='Ourives')
    CategoriaServico.objects.create(nome='Padeiro')
    CategoriaServico.objects.create(nome='Paisagista')
    CategoriaServico.objects.create(nome='Palestrante')
    CategoriaServico.objects.create(nome='Panfleteiro')
    CategoriaServico.objects.create(nome='Passador')
    CategoriaServico.objects.create(nome='Pedagogo')
    CategoriaServico.objects.create(nome='Pedreiro')
    CategoriaServico.objects.create(nome='Peixeiro')
    CategoriaServico.objects.create(nome='Perfumista')
    CategoriaServico.objects.create(nome='Perito Judicial')
    CategoriaServico.objects.create(nome='Personal Stylist')
    CategoriaServico.objects.create(nome='Personal Trainer')
    CategoriaServico.objects.create(nome='Pesador')
    CategoriaServico.objects.create(nome='Pesquisador')
    CategoriaServico.objects.create(nome='Pesquisador de Mercado')
    CategoriaServico.objects.create(nome='Piloteiro')
    CategoriaServico.objects.create(nome='Piloto')
    CategoriaServico.objects.create(nome='Pintor')
    CategoriaServico.objects.create(nome='Pintor')
    CategoriaServico.objects.create(nome='Pizzaiolo')
    CategoriaServico.objects.create(nome='Planejador de Produção')
    CategoriaServico.objects.create(nome='Planejador de Projetos')
    CategoriaServico.objects.create(nome='Podólogo')
    CategoriaServico.objects.create(nome='Polidor')
    CategoriaServico.objects.create(nome='Porteiro')
    CategoriaServico.objects.create(nome='Prensista')
    CategoriaServico.objects.create(nome='Preparador')
    CategoriaServico.objects.create(nome='Processista')
    CategoriaServico.objects.create(nome='Produtor')
    CategoriaServico.objects.create(nome='Professor')
    CategoriaServico.objects.create(nome='Programador')
    CategoriaServico.objects.create(nome='Projetista')
    CategoriaServico.objects.create(nome='Promotor')
    CategoriaServico.objects.create(nome='Propagandista')
    CategoriaServico.objects.create(nome='Protético')
    CategoriaServico.objects.create(nome='Psicólogo')
    CategoriaServico.objects.create(nome='Psicomotricista')
    CategoriaServico.objects.create(nome='Psicopedagogo')
    CategoriaServico.objects.create(nome='Publicitário')
    CategoriaServico.objects.create(nome='Químico')
    CategoriaServico.objects.create(nome='Radialista')
    CategoriaServico.objects.create(nome='Rasteleiro')
    CategoriaServico.objects.create(nome='Rebarbador de Metais')
    CategoriaServico.objects.create(nome='Rebobinador')
    CategoriaServico.objects.create(nome='Recebedor')
    CategoriaServico.objects.create(nome='Recepcionista')
    CategoriaServico.objects.create(nome='Recreador')
    CategoriaServico.objects.create(nome='Recuperador de Crédito')
    CategoriaServico.objects.create(nome='Redator')
    CategoriaServico.objects.create(nome='Regulador de Sinistros')
    CategoriaServico.objects.create(nome='Relações Públicas')
    CategoriaServico.objects.create(nome='Relojoeiro')
    CategoriaServico.objects.create(nome='Repórter')
    CategoriaServico.objects.create(nome='Repositor')
    CategoriaServico.objects.create(nome='Repositor de Perecíveis')
    CategoriaServico.objects.create(nome='Representante Comercial')
    CategoriaServico.objects.create(nome='Retificador')
    CategoriaServico.objects.create(nome='Revisor')
    CategoriaServico.objects.create(nome='Rigger')
    CategoriaServico.objects.create(nome='Robotista')
    CategoriaServico.objects.create(nome='Roteirista')
    CategoriaServico.objects.create(nome='Roteirizador')
    CategoriaServico.objects.create(nome='Saladeiro')
    CategoriaServico.objects.create(nome='Salgadeiro')
    CategoriaServico.objects.create(nome='Salva Vidas')
    CategoriaServico.objects.create(nome='Sapateiro')
    CategoriaServico.objects.create(nome='Scouter')
    CategoriaServico.objects.create(nome='Scrum Master')
    CategoriaServico.objects.create(nome='Secretária')
    CategoriaServico.objects.create(nome='Segurança')
    CategoriaServico.objects.create(nome='Selecionador')
    CategoriaServico.objects.create(nome='Separador de Mercadorias')
    CategoriaServico.objects.create(nome='Serralheiro')
    CategoriaServico.objects.create(nome='Servente de Obras')
    CategoriaServico.objects.create(nome='Sinaleiro')
    CategoriaServico.objects.create(nome='Síndico')
    CategoriaServico.objects.create(nome='Sociólogo')
    CategoriaServico.objects.create(nome='Socorrista')
    CategoriaServico.objects.create(nome='Soldador')
    CategoriaServico.objects.create(nome='Soldador Montador')
    CategoriaServico.objects.create(nome='Sommelier')
    CategoriaServico.objects.create(nome='Sondador')
    CategoriaServico.objects.create(nome='Sonoplasta')
    CategoriaServico.objects.create(nome='Sorveteiro')
    CategoriaServico.objects.create(nome='Steward')
    CategoriaServico.objects.create(nome='Superintendente')
    CategoriaServico.objects.create(nome='Supervisor')
    CategoriaServico.objects.create(nome='Suporte Técnico')
    CategoriaServico.objects.create(nome='Sushiman')
    CategoriaServico.objects.create(nome='Tapeceiro')
    CategoriaServico.objects.create(nome='Tecelão')
    CategoriaServico.objects.create(nome='Técnico')
    CategoriaServico.objects.create(nome='Tecnólogo')
    CategoriaServico.objects.create(nome='Telefonista')
    CategoriaServico.objects.create(nome='Telhadista')
    CategoriaServico.objects.create(nome='Terapeuta Ocupacional')
    CategoriaServico.objects.create(nome='Tesoureiro')
    CategoriaServico.objects.create(nome='Tintureiro')
    CategoriaServico.objects.create(nome='Topógrafo')
    CategoriaServico.objects.create(nome='Torneiro')
    CategoriaServico.objects.create(nome='Tosador')
    CategoriaServico.objects.create(nome='Traçador de Caldeiraria')
    CategoriaServico.objects.create(nome='Trader')
    CategoriaServico.objects.create(nome='Tradutor')
    CategoriaServico.objects.create(nome='Trainee')
    CategoriaServico.objects.create(nome='Tratador de Piscina')
    CategoriaServico.objects.create(nome='Tratorista')
    CategoriaServico.objects.create(nome='Trefilador')
    CategoriaServico.objects.create(nome='Trocador de Moldes')
    CategoriaServico.objects.create(nome='Turismólogo')
    CategoriaServico.objects.create(nome='Vendedor')
    CategoriaServico.objects.create(nome='Veterinário')
    CategoriaServico.objects.create(nome='Videografista')
    CategoriaServico.objects.create(nome='Vidraceiro')
    CategoriaServico.objects.create(nome='Vigia')
    CategoriaServico.objects.create(nome='Vigilante')
    CategoriaServico.objects.create(nome='Visitador de Navios')
    CategoriaServico.objects.create(nome='Vistoriador')
    CategoriaServico.objects.create(nome='Visual Merchandiser')
    CategoriaServico.objects.create(nome='Vitrinista')
    CategoriaServico.objects.create(nome='Web Designer')
    CategoriaServico.objects.create(nome='Web Developer')
    CategoriaServico.objects.create(nome='Webmaster')
    CategoriaServico.objects.create(nome='Zelador')
    CategoriaServico.objects.create(nome='Zootecnista')
