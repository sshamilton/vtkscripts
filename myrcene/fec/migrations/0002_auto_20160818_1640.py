# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-18 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fec', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='param1',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='task',
            name='param2',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='task',
            name='param3',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='task',
            name='param4',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='task',
            name='param5',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='task',
            name='spawned',
            field=models.BooleanField(default=False),
        ),
    ]
