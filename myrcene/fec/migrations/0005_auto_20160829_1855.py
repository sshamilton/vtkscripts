# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 18:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fec', '0004_task_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='avg_cube_time',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='result',
            name='total_time',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='task',
            name='param1',
            field=models.CharField(blank=True, default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='task',
            name='param2',
            field=models.CharField(blank=True, default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='task',
            name='param3',
            field=models.CharField(blank=True, default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='task',
            name='param4',
            field=models.CharField(blank=True, default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='task',
            name='param5',
            field=models.CharField(blank=True, default=b'', max_length=200),
        ),
    ]
