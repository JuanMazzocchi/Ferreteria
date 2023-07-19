from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# Create your models here.

# class ArchivoCSV(models.Model):
#     archivo=models.FileField(upload_to='uploads',storage=OverwriteStorage(), verbose_name='Archivo')
    
class OverwriteStorage(FileSystemStorage):
    '''
    Cambia el comportamiento predeterminado de Django y hace que sobrescriba los archivos fuente del
    mismo nombre que fueron subidos por el usuario en lugar de cambiarles el nombre.
    '''
    def get_available_name(self,nombre,max_length=None):
        if self.exists(nombre):
           os.remove(os.path.join(self.location, nombre))
        return nombre
 
class ArchivoCSV(models.Model):
    nombre=models.CharField(verbose_name='nombre', max_length=128, default='None')
    archivo=models.FileField(upload_to='uploads',storage=OverwriteStorage(), verbose_name='Archivo')
       
class ListaDePrecios(models.Model):
    nombre=models.CharField(verbose_name='nombre', max_length=128, default='None')
    archivo=models.FileField(verbose_name='Nombre', upload_to=settings.MEDIA_DIR, storage=OverwriteStorage(), default="None")
    

class prueba(models.Model):
    prueba=models.CharField(verbose_name="Prueba", max_length=100)   