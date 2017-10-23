import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, UserManager
from django.core import validators
from django.conf import settings
import datetime

class User(AbstractBaseUser, PermissionsMixin):


    email = models.EmailField('E-mail', unique=True)
    username = models.CharField('Usuário', max_length=100, blank=True)
    # nome = models.CharField('Nome completo', max_length=100, null=True)
    telefone = models.CharField('Telefone', max_length=15, default=True)
    cpf = models.CharField('CPF', max_length=14, unique=True, default=True)
    sexo = models.CharField('Sexo', max_length=9, default=True)
    rua = models.CharField('Rua', max_length=50, default=True)
    numero = models.CharField('Número', max_length=15, default=True)
    bairro = models.CharField('Bairro', max_length=50, default=True)
    cidade = models.CharField('Cidade', max_length=50, default=True)
    estado = models.CharField('Estado', max_length=50, default=True)

    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
    date_joined = models.DateTimeField(
        'Data de entrada', auto_now_add=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email' #padrao para login
    REQUIRED_FIELDS = ['username'] #utilizado pra criaçao de superusuario

    def __str__(self):  #se tem nome retorna nome
        return self.name or self.username

    def get_short_name(self): #para funcionamento do admin
        return self.email

    def get_full_name(self): #representação em string do objeto
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class PasswordReset(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        # related_name='resets'
    )

    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank =True)

    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']
