import re
from django.db import models
from trabalhocom.accounts.models import User
from django.core import validators

class Service(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    descricao_servico = models.CharField('Descrição/Serviço', max_length=100, default=True)
    tempo_experiencia = models.IntegerField('Tempo de Experiência', default=True)
    unid_tempo = models.CharField(max_length=5, null=False, default=True)
    descricao_exp = models.TextField('Descrição/Experiencia', max_length=400, default=True)


   #categoria =

    def __str__(self):
        return self.descricao_servico


    class Meta:
        verbose_name = 'Novo serviço'
        verbose_name_plural = 'Novos Serviços'
