from django.db import models

# Create your models here.

class ArchivoCSV(models.Model):
    archivo=models.FileField(upload_to='uploads', verbose_name='Archivo')
    
    