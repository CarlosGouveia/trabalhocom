# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 05:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20171023_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nome',
            field=models.CharField(max_length=100, null=True, verbose_name='Nome completo'),
        ),
    ]
