# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genderwatch', '0003_auto_20170723_1156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assembly',
            options={'ordering': ['date'], 'verbose_name': 'Versammlung', 'verbose_name_plural': 'Versammlungen'},
        ),
        migrations.RemoveField(
            model_name='assembly',
            name='group',
        ),
        migrations.AlterField(
            model_name='event',
            name='gender',
            field=models.CharField(choices=[('m', 'Männer*'), ('f', 'Frauen*'), ('a', 'Andere')], max_length=2, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='verdict',
            name='category',
            field=models.CharField(blank=True, choices=[('OR', 'Organisatorisch'), ('WI', 'Wirtschaft'), ('FI', 'Finanzen'), ('UW', 'Umwelt'), ('CA', 'Care'), ('AR', 'Arbeit'), ('ST', 'Staat'), ('MI', 'Migration')], max_length=2, verbose_name='Kategorie'),
        ),
        migrations.AlterField(
            model_name='verdict',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'Männer*'), ('f', 'Frauen*'), ('a', 'Andere')], max_length=2, verbose_name='Gender'),
        ),
    ]
