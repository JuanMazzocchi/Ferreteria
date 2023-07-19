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
            
        if  e == valor:     
            return True
        else:
            pass 
    return False

@register.filter()
def prueba(value):
    print('funciona')
    return value