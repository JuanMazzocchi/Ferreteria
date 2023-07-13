from django import forms

from Portal.models import Producto
from Administrador.models import ArchivoCSV


class ProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields='__all__'   #cambiar luego, poner los campos deseados solamente
        


class SearchForm(forms.Form):
    keyword=forms.CharField(max_length=150, label='Palabra/Codigo a buscar',widget=forms.TextInput(attrs={'placeholder':'codigo, descipcion, linea, rubro',"size": "100"}))


class SearchServicioForm(forms.Form):
            keyword=forms.CharField(max_length=150, label='Palabra a buscar',widget=forms.TextInput(attrs={'placeholder':' descipcion ',"size": "100"}))

class SearchClienteForm(forms.Form):
            keyword=forms.CharField(max_length=150, label='Nombre o Apellido a buscar', widget=forms.TextInput(attrs={'placeholder':'nombre o apellido',"size": "100"}) )
            
class ArchivoCSVForm(forms.Form):     #no esta en uso
    class Meta:                   
        model=ArchivoCSV
        fields='__all__'
        