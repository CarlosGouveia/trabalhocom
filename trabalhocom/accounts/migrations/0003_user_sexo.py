# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 03:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20171023_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sexo',
            field=models.CharField(default=True, max_length=9, verbose_name='Sexo'),
        ),
    ]
