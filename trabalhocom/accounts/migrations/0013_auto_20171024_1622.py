# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_user_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sexo',
            field=models.CharField(choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino')], default=True, max_length=9, verbose_name='Sexo'),
        ),
        migrations.AlterField(
            model_name='user',
            name='telefone',
            field=models.CharField(default=True, help_text='Use o seguinte formato: <em> (99) 9999-9999 </ em>.', max_length=15, verbose_name='Telefone'),
        ),
    ]