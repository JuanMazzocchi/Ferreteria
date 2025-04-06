import re
from django import forms
from django.forms import ValidationError
 

#Validaciones para el formulario
def validate_name(value):
  nombre_regex = r'^[a-zA-ZÀ-ÿ\s]{4,40}$'
  if not re.match(nombre_regex, value):
    raise ValidationError('El nombre ingresado es invalido')

def validate_email(value):
  email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
  if not re.match(email_regex, value):
    raise ValidationError('El email ingresado es invalido.')
  
def max_number_validation(value):
  number = str(value)
  if len(number) != 10:
    raise ValidationError('El numero debe contener 10 digitos.')

#La clase formulario
class FormularioContacto(forms.Form):

  nombreContacto = forms.CharField(
    label='Nombre', 
    max_length=40,
    validators=[validate_name],
    required= True,
    error_messages={
      'required': 'Por favor completa el campo'
    },
    widget=forms.TextInput(
      attrs={'class': 'form-control col-12 my-2 text-center',
             'placeholder': 'Ingrese su nombre',
             'pattern':'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$'}
    )
  )
  
  emailContacto = forms.EmailField(
    label='Email', 
    max_length=50,
    validators=[validate_email],
    required= True,
    error_messages={
      'required': 'Por favor completa el campo'
    },
    widget=forms.EmailInput(
      attrs={'class': 'form-control col-12 my-2 text-center',
             'placeholder': 'Ingrese su mail'}
    )
  )

  telefonoContacto = forms.CharField(
    label='Telefono', 
    max_length=15,
    validators=[max_number_validation],
    required= True,
    widget=forms.TextInput(
      attrs={'class': 'form-control col-12 my-2 text-center',
              'placeholder': 'Ingrese su telefono',
              'pattern':'^[0-9]*$'}
    )
  )

  mensajeContacto = forms.CharField(
    label='Mensaje', 
    max_length=50,
    required= True,
    widget=forms.Textarea(
      attrs={'class': 'form-control col-12 my-2',
             'placeholder': 'Ingrese su mensaje aca...'}
    )
  )

class LoginForm(forms.Form):
      
  username=forms.CharField(
    max_length=50,
    label='Nombre',
    required= True,
    widget=forms.TextInput(
      attrs={'class': 'form-control my-2 text-center',
             'placeholder': 'Ingrese su nombre',
             'autocomplete': 'username'}
    )
  )

  password=forms.CharField(
    max_length=50,
    label='Contraseña',
    required= True,
    widget=forms.PasswordInput(
      attrs={'class': 'form-control my-2 text-center',
             'placeholder': 'Ingrese su contraseña',
             'autocomplete': 'current-password'}
    )
  )