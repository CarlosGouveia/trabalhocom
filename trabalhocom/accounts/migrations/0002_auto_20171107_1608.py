# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-07 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rg',
            field=models.CharField(default=True, max_length=13, unique=True, verbose_name='RG'),
        ),
    ]