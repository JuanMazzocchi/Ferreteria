# Generated by Django 3.2 on 2023-07-19 17:07

import Administrador.models
from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivoCSV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='uploads', verbose_name='Archivo')),
            ],
        ),
        migrations.CreateModel(
            name='ListaDePrecios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='None', max_length=128, verbose_name='nombre')),
                ('archivo', models.FileField(default='None', storage=Administrador.models.OverwriteStorage(), upload_to=pathlib.PureWindowsPath('C:/Users/juanm/OneDrive/Escritorio/grupo 2/grupo2-django/uploads'), verbose_name='Nombre')),
            ],
        ),
    ]