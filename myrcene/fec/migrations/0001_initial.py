# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('maxcubes', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('xlen', models.IntegerField(default=1)),
                ('ylen', models.IntegerField(default=1)),
                ('zlen', models.IntegerField(default=1)),
                ('ghostcells', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_cube', models.IntegerField(default=0)),
                ('last_cube', models.IntegerField(default=0)),
                ('total_time', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(verbose_name=b'created at')),
                ('modified_at', models.DateTimeField(verbose_name=b'modified at')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.IntegerField(default=0)),
                ('cube_start', models.IntegerField(default=0)),
                ('cube_end', models.IntegerField(default=0)),
                ('completed_cubes', models.IntegerField(default=0)),
                ('input_file', models.CharField(max_length=200)),
                ('output_file', models.CharField(max_length=200)),
                ('host', models.ForeignKey(to='fec.Host')),
                ('job', models.ForeignKey(to='fec.Job')),
                ('modules', models.ForeignKey(to='fec.Module')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='task',
            field=models.ForeignKey(to='fec.Task'),
        ),
    ]
