from django.conf.urls import include, url
from trabalhocom.services import views


urlpatterns = [
    url(r'^meus-servicos/$', views.myservices, name='myservices'),
    url(r'^cadastrar-servico/$', views.register_services, name='register_services'),
    url(r'^buscar-todos-servicos/$', views.search_All_services, name='search-ALL-services'),
    # url(r'^buscar-servicos/$', views.search_services, name='search-services'),
    url(r'^meus-servico-editar/$', views.myservices_list_update, name='myservices_list_update'),
    url(r'^(?P<pk>\d+)/$', views.edit_services, name='edit_services'),
    url(r'^detalhes-busca/$', views.detail_search, name='detail_search'),
    url(r'^mais-detalhes(?P<pk>\d+)/$', views.mais_detalhes, name='mais_detalhes'),
]

# url(r'^(?P<pk>\d+)/$'