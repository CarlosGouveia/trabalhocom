# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cpf',
            field=models.CharField(default=True, max_length=12, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nome',
            field=models.CharField(default=True, max_length=100, verbose_name='Nome completo'),
        ),
    ]
