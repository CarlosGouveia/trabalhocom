from django.conf.urls import url
from trabalhocom.core import views


urlpatterns = [
    url(r'^$', views.home, name='home'),

]