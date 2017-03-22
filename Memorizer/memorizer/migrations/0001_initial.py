# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('numMemorized', models.IntegerField(default=0)),
                ('streak', models.IntegerField(default=0)),
            ],
        ),
    ]
