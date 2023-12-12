from django.db import models

# Create your models here.


#uno a uno

class Producto(models.Model):
    
           
    cod_producto=models.CharField(max_length=20, verbose_name='Cod. Producto')
    descripcion=models.CharField(max_length=200, verbose_name='Descripcion')
    pcio_lista=models.FloatField(max_length=20, verbose_name='Precio de Lista')
    unidad=models.CharField(max_length=50, verbose_name='Unidad')
    imagen=models.CharField(max_length=10, verbose_name='Imagen',null=True)
    linea=models.CharField(max_length=100, verbose_name='Linea')
    rubro=models.CharField(max_length=50, verbose_name='Rubro')
    ordenLinea=models.CharField(max_length=10, verbose_name='Orden de Linea')
    ordenRubro=models.CharField(max_length=10, verbose_name='Orden de Rubros')
    
    
    def __str__(self):
        return f' {self.cod_producto} - {self.rubro} - {self.linea} - {self.descripcion} - {self.pcio_lista} - {self.unidad} - {self.imagen}'
    
    
   
  #muchos a uno
class Linea_servicio(models.Model):
    
    linea=models.CharField(max_length=100 , verbose_name='Linea')
    
    def __str__(self):
        return f"{self.linea}"
    
    
class Servicio(models.Model):
    
    descripcion=models.CharField(max_length=100 , verbose_name='Descripcion')       
    pcio_lista=models.FloatField(max_length=10 , verbose_name='Precio')
    linea=models.ForeignKey(Linea_servicio, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.descripcion} - {self.pcio_lista} - {self.linea}'
    
    
#muchos a muchos

class Cliente(models.Model):
    
    nombre=models.CharField(max_length=50, verbose_name='Nombre')
    apellido=models.CharField(max_length=50 , verbose_name='Apellido')
    email=models.CharField(max_length=50 , verbose_name='Email')
    
    
    def __str__(self):
        return f'{self.nombre} - {self.apellido} - {self.email}'
    
    
class Metodo_de_pago(models.Model):
    
    tipo=models.CharField( max_length=50 , verbose_name='Metodo de Pago')
    cliente=models.ManyToManyField(Cliente)
    
    def __str__(self):
        return f'{self.tipo} '