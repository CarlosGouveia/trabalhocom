# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-07 01:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaServico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default=True, max_length=100, verbose_name='Nome categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao_servico', models.CharField(default=True, max_length=100, verbose_name='Descrição/Serviço')),
                ('tempo_experiencia', models.IntegerField(default=True, verbose_name='Tempo de Experiência')),
                ('unid_tempo', models.CharField(default=True, max_length=2, verbose_name='Unidade de medida')),
                ('descricao_exp', models.TextField(default=True, max_length=400, verbose_name='Descrição/Experiencia')),
                ('valor', models.DecimalField(decimal_places=2, default=True, max_digits=10, verbose_name='Valor')),
                ('valor_servico', models.CharField(default=True, max_length=3, verbose_name='Valor serviço')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.CategoriaServico')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Novo serviço',
                'verbose_name_plural': 'Novos Serviços',
            },
        ),
    ]
