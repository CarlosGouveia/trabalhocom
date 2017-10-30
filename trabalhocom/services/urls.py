from django.conf.urls import include, url
from trabalhocom.services import views


urlpatterns = [
    url(r'^meus-servicos/$', views.myservices, name='myservices'),
    url(r'^cadastrar-servico/$', views.register_services, name='register_services'),
    url(r'^buscar-profissionais/$', views.search_professionals, name='search-professionals'),
    # url(r'^editar-servico/$', views.edit_services, name='edit_services'),
    url(r'^meus-servico-editar/$', views.myservices_list_update, name='myservices_list_update'),
    url(r'^(?P<pk>\d+)/$', views.edit_services, name='edit_services'),
]

# url(r'^(?P<pk>\d+)/$'