# Generated by Django 3.2 on 2023-07-22 21:55

import Administrador.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administrador', '0014_alter_archivocsv_archivo'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoPorMail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(help_text='Archivo .xlsx para enviar pedidos por mail por parte de los clientes', storage=Administrador.models.OverwriteStorage(), upload_to=Administrador.models.user_directory_path_PedidoPorMail, verbose_name='Archivo')),
            ],
        ),
    ]