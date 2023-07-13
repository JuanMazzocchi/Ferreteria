from django import template
from django.template.defaultfilters import stringfilter
from ..views import listaDeImagenes
import re

register=template.Library()

@register.filter()
@stringfilter
def existeLaImg(value):
    listadoDeImagenes=listaDeImagenes()
    # valor=str(value)
    valor=str(value)
    for e in listadoDeImagenes:
           
 
        if  e == valor[:-1]:    #el valor trae un salto de linea invisible en el ultimo caracter asi que lo recorto para comparar
            return True
        else:
            pass 
    return False

@register.filter()
def prueba(value):
    print('funciona')
    return value