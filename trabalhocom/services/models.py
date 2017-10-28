from django.db import models

class CreateService(models.Model):

    valor = models.FloatField('Valor')
    descricao = models.TextField('Descrição', max_length=400)
    data_inicio = models.DateField()
   #categoria =

    class Meta:
        verbose_name = 'Novo serviço'
        verbose_name_plural = 'Novos Serviços'
