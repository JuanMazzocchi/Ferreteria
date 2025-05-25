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
    return 'uploads/{0}'.format('ListaDePrecios.xlsx')

def user_directory_path_CSV(instance, filename):
    # le doy siempre el mismo nombre al archivo de la Base de datos .CSV
    return 'uploads/{0}'.format('BaseDeDatos.csv')

def user_directory_path_PedidoPorMail(instance, filename):
    return 'uploads/{0}'.format('Catalogo.pdf')

def user_directory_path_CatalogoSanitarios(instance, filename):
    return 'uploads/{0}'.format('CatalogoSanitarios.pdf')

def user_directory_path_CatalogoGas(instance, filename):
    return 'uploads/{0}'.format('CatalogoGas.pdf')

def user_directory_path_CatalogoFerreteria(instance, filename):
    return 'uploads/{0}'.format('CatalogoFerreteria.pdf')

def user_directory_path_CatalogoBronce(instance, filename):
    return 'uploads/{0}'.format('CatalogoBronce.pdf')

def user_directory_path_CatalogoPPN(instance, filename):
    return 'uploads/{0}'.format('CatalogoPPN.pdf')

def user_directory_path_CatalogoThermofusion(instance, filename):
    return 'uploads/{0}'.format('CatalogoThermofusion.pdf')

def user_directory_path_CatalogoEpoxi(instance, filename):
    return 'uploads/{0}'.format('CatalogoEpoxi.pdf')

def user_directory_path_CatalogoSigas(instance, filename):
    return 'uploads/{0}'.format('CatalogoSigas.pdf')


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
    archivo=models.FileField(verbose_name='Archivo', upload_to=user_directory_path_PedidoPorMail, storage=OverwriteStorage(), help_text="Archivo .pdf del catalogo")

class ListaPrioritariaDeLineas(models.Model):
    archivo=models.CharField(max_length=500, verbose_name='Lista')
    
class CatalogoSanitarios(models.Model):
    archivo=models.FileField(verbose_name='Sanitarios',upload_to=user_directory_path_CatalogoSanitarios, storage=OverwriteStorage(), help_text="Archivo .pdf del catalogo de Sanitarios")
    
class CatalogoGas(models.Model):
    archivo=models.FileField(verbose_name='Gas',upload_to=user_directory_path_CatalogoGas, storage=OverwriteStorage(), help_text="Archivo .pdf del catalogo de Gas")

class CatalogoFerreteria(models.Model):
    archivo=models.FileField(verbose_name='Ferreteria',upload_to=user_directory_path_CatalogoFerreteria, storage=OverwriteStorage(), help_text="Archivo .pdf del catalogo de Ferreteria")    
    
class CatalogoBronce(models.Model):
    archivo=models.FileField(verbose_name='Bronce',upload_to=user_directory_path_CatalogoBronce, storage=OverwriteStorage(), help_text="Archivo .pdf del catalogo de Bronce Roscado")    
    
class CatalogoPPN(models.Model):
    archivo=models.FileField(verbose_name='PPN',upload_to=user_directory_path_CatalogoPPN, storage=OverwriteStorage(), help_text="Archivo .pdf del catalogo de PPN Espiga")    

class CatalogoThermofusion(models.Model):
    archivo=models.FileField(verbose_name='Thermofusion',upload_to=user_directory_path_CatalogoThermofusion, storage=OverwriteStorage(), help_text="Archivo .pdf del catalogo de Thermofusion")    
    
class CatalogoEpoxi(models.Model):
    archivo=models.FileField(verbose_name='Epoxi',upload_to=user_directory_path_CatalogoEpoxi, storage=OverwriteStorage(), help_text="Archivo .pdf del catalogo de Epoxi")    
    
class CatalogoSigas(models.Model):
    archivo=models.FileField(verbose_name='Sigas',upload_to=user_directory_path_CatalogoSigas, storage=OverwriteStorage(), help_text="Archivo .pdf del catalogo de Sigas")    