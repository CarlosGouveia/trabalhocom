import re
from django.db import models
from trabalhocom.accounts.models import User
from django.core import validators

class Service(models.Model):

    TEMPO_CHOICES = (
        (u'ME', u'Mês(es)'),
        (u'AN', u'Ano(s)'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    descricao_servico = models.CharField('Descrição/Serviço', max_length=100, default=True)
    tempo_experiencia = models.IntegerField('Tempo de Experiência', default=True)
    unid_tempo = models.CharField(max_length=2, null=False, default=True)
    descricao_exp = models.TextField('Descrição/Experiencia', max_length=400, default=True)
    valor = models.FloatField('Valor', default=True)
    #valor = models.CharField('Valor', max_length=5, default=True)
    # valor = models.CharField(
    #     'Valor',  blank=True,
    #     validators=[validators.RegexValidator(re.compile('^\d+(?:\.\d{1,2})?$'), 'Use a formatação correta do valor decimal(Ex: 0.00).')])

    # valor = models.DecimalField('Valor', decimal_places=2, max_digits=9, blank=True)
    #valor = models.FloatField('Valor')
    descricao = models.TextField('Descrição', max_length=400)
    data_inicio = models.DateField()
    #categoria =

    def __str__(self):
        return self.descricao_servico


    class Meta:
        verbose_name = 'Novo serviço'
        verbose_name_plural = 'Novos Serviços'
