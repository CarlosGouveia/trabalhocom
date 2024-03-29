import re
from django.db import models
from trabalhocom.accounts.models import User
from django.core import validators

class CategoriaServico(models.Model):

    nome = models.CharField('Nome categoria', max_length=100, default=True)

    def __str__(self):
        return self.nome

# class Comment(models.Model):
#     post = models.ForeignKey('blog.Post', related_name='comments')
#     author = models.CharField(max_length=200)
#     text = models.TextField()
#     created_date = models.DateTimeField(default=timezone.now)
#     approved_comment = models.BooleanField(default=False)

    # def approve(self):
    #     self.approved_comment = True
    #     self.save()
    #
    # def __str__(self):
    #     return self.text


class Service(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    descricao_servico = models.CharField('Descrição/Serviço', max_length=100, default=True)
    tempo_experiencia = models.IntegerField('Tempo de Experiência', default=True)

    unid_tempo = models.CharField(max_length=5, null=False, default=True)
    descricao_exp = models.TextField('Descrição/Experiencia', max_length=400, default=True)

    categoria = models.ForeignKey(CategoriaServico, on_delete=models.CASCADE)
    unid_tempo = models.CharField('Unidade de medida', max_length=2, null=False, default=True)
    descricao_exp = models.TextField('Descrição/Experiencia', max_length=400, default=True)
    valor = models.DecimalField('Valor', decimal_places=2 , max_digits=10, default=True)
    valor_servico = models.CharField('Valor serviço', max_length=3, default=True)

    def __str__(self):
        return self.descricao_servico


    class Meta:
        verbose_name = 'Novo serviço'
        verbose_name_plural = 'Novos Serviços'
