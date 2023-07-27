from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os, re
from django.forms import ValidationError

# Create your models here.
    
class OverwriteStorage(FileSystemStorage):
    '''
    Cambia el comportamiento predeterminado de Django y hace que sobrescriba los archivos fuente del
    mismo nombre que fueron subidos por el usuario en lugar de cambiarles el nombre.
    '''
    def get_available_name(self,nombre,max_length=None):
        if self.exists(nombre):
                   os.remove(os.path.join(self.location, nombre))
        return nombre
    
def user_directory_path(instance, filename):
    # le doy siempre el mismo nombre al archivo de la lista de precios
    return 'uploads/{0}'.format('lista.xlsx')

def user_directory_path_CSV(instance, filename):
    # le doy siempre el mismo nombre al archivo de la Base de datos .CSV
    return 'uploads/{0}'.format('BaseDeDatos.csv')

def user_directory_path_PedidoPorMail(instance, filename):
    return 'uploads/{0}'.format('PedidoPorMail.xlsx')

def validate_csv(value):
     
    if (not value.name.endswith('.csv')):
        raise ValidationError('El archivo no es .csv')

class ArchivoCSV(models.Model):
    archivo=models.FileField(validators=[validate_csv] , upload_to=user_directory_path_CSV,storage=OverwriteStorage(), verbose_name='Archivo')
       
class ListaDePrecios(models.Model):
    archivo=models.FileField(verbose_name='Archivo',upload_to=user_directory_path, storage=OverwriteStorage(), default="None")
    

class FotosDeProductos(models.Model):
    archivo=models.ImageField(upload_to='img',storage=OverwriteStorage(), null=True, help_text="Ejemplo: 111111.jpg")   


class PedidoPorMail(models.Model):
    archivo=models.FileField(verbose_name='Archivo', upload_to=user_directory_path_PedidoPorMail, storage=OverwriteStorage(), help_text="Archivo .xlsx para enviar pedidos por mail por parte de los clientes")