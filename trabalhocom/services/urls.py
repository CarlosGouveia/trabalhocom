from django.conf.urls import include, url
from trabalhocom.services import views


urlpatterns = [
    url(r'^meus-servicos/$', views.myservices, name='myservices'),
    url(r'^meus-servicos-detalhes(?P<pk>\d+)/$', views.myservices_details, name='myservices-details'),
    url(r'^cadastrar-servico/$', views.register_services, name='register_services'),
    url(r'^buscar-todos-servicos/$', views.search_All_services, name='search-ALL-services'),
    # url(r'^buscar-todos-servicos/$', views.services, name='search-ALL-services'),
    # url(r'^buscar-servicos/$', views.search_services, name='search-services'),
    url(r'editar-servico(?P<pk>\d+)/$', views.edit_services, name='edit_services'),
    #url(r'^detalhes-busca/$', views.detail_search, name='detail_search'),
    url(r'^mais-detalhes(?P<pk>\d+)/$', views.mais_detalhes, name='mais_detalhes'),
    url(r'^entrar/$', views.login_view_services, name='login'),
    url(r'^remover-servico/(?P<pk>\d+)/$', views.service_remove, name='service_remove'),
]

# url(r'^(?P<pk>\d+)/$'