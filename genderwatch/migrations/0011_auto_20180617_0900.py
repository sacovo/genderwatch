# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-17 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genderwatch', '0010_auto_20171015_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assembly',
            name='category',
            field=models.CharField(choices=[('DV', 'Delegiertenversammlung'), ('SEKO', 'Sektionskonferenz'), ('JV', 'Jahresversammlung'), ('BV', 'Bildungsveranstaltung'), ('VV', 'Vollversammlung'), ('MV', 'Mitgliederversammlung'), ('GRS', 'Grossratssitzung'), ('KRS', 'Kantonsratssitzung'), ('NRS', 'Nationalratssitzung'), ('SRS', 'Ständeratssitzung'), ('STRS', 'Stadtratssitzung'), ('GERS', 'Gemeinderatssitzung'), ('ERS', 'Einwohnerratssitzung')], max_length=10, verbose_name='Kategorie'),
        ),
        migrations.AlterField(
            model_name='event',
            name='position',
            field=models.CharField(choices=[('GL', 'Geschäftsleitung'), ('PR', 'Präsidium'), ('VS', 'Vorstand'), ('BA', 'Basis'), ('DG', 'Delegierte'), ('GA', 'Gäst*innen'), ('PO', 'Podium'), ('NR', 'Nationalrat'), ('BR', 'Bundesrat'), ('SR', 'Ständerat'), ('KR', 'Kantonsrat'), ('GR', 'Grossrat'), ('LR', 'Landrat'), ('RR', 'Regierungsrat'), ('STR', 'Stadtrat'), ('GER', 'Gemeinderat'), ('ER', 'Einwohnerrat')], max_length=2, verbose_name='Position'),
        ),
        migrations.AlterField(
            model_name='verdict',
            name='position',
            field=models.CharField(blank=True, choices=[('GL', 'Geschäftsleitung'), ('PR', 'Präsidium'), ('VS', 'Vorstand'), ('BA', 'Basis'), ('DG', 'Delegierte'), ('GA', 'Gäst*innen'), ('PO', 'Podium'), ('NR', 'Nationalrat'), ('BR', 'Bundesrat'), ('SR', 'Ständerat'), ('KR', 'Kantonsrat'), ('GR', 'Grossrat'), ('LR', 'Landrat'), ('RR', 'Regierungsrat'), ('STR', 'Stadtrat'), ('GER', 'Gemeinderat'), ('ER', 'Einwohnerrat')], max_length=2, verbose_name='Position'),
        ),
    ]
