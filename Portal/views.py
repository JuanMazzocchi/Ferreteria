from django.shortcuts import render, redirect
from django.conf import settings
from .forms import FormularioContacto
from Portal.models import *
from django.views.generic.list import ListView
from Portal.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import os
from pathlib import Path


@login_required
def home(request):
                       
    return render(request, 'Portal/home.html')

def contacto(request):
     
    if request.method == 'POST':
        formulario_contacto = FormularioContacto(request.POST)
        
        return redirect('loginView')
                        
    else:
        
        formulario_contacto = FormularioContacto()

    context = {
        'formulario_contacto': formulario_contacto,
    }

    return render(request, 'Portal/contacto.html', context)

@login_required
def lineas(request):
 
    lineas=Producto.objects.order_by().values_list('linea',flat=True).distinct()
    context={'lineas':lineas}
    # print(context)
    
    return render(request, 'Portal/mostrarLineas.html', context  )

def about(request):
    return render(request, 'Portal/about.html')

@login_required
def seleccion(request,linea):   
           
        rubro=Producto.objects.order_by().values_list('rubro', flat=True).distinct().filter(linea=linea)
        # print(rubro)
        imagenes=[]
        listaDeRubros=[]
        
        for item in rubro:
            # print(item)
            listaDeRubros.append(item)
            
            imagen=Producto.objects.distinct().filter(rubro=item)[0]
            # print(imagen.imagen)
            imagenes.append(imagen.imagen)
        
        # print(imagenes)
        diccionario=dict(zip(listaDeRubros,imagenes))
        # print(diccionario)
        listadoDeImagenes=listaDeImagenes()
         
        context={'rubros':rubro, 'diccionarios':diccionario, 'listadoDeImagenes': listadoDeImagenes}
        return render(request,'Portal/mostrarRubros.html', context)
    
@login_required    
def gondola(request,rubro):
       
    articulos=Producto.objects.all().filter(rubro=rubro)
    context={'articulos':articulos}
    # print(articulos)
    return render(request,'Portal/mostrarArticulos.html' ,context )

@login_required
def portalSearch(request):
    
    if request.method =='GET':
        
        keyword=request.GET.get('keyword')
        cod=Producto.objects.all().filter(cod_producto__contains=keyword)
        linea=Producto.objects.all().filter(linea__icontains=keyword)
        rubro=Producto.objects.all().filter(rubro__icontains=keyword)
        desc=Producto.objects.all().filter(descripcion__icontains=keyword)
        articulos=cod.union(linea,rubro,desc)
        context ={'articulos':articulos }
        # print(articulos)
        return render(request,'Portal\mostrarArticulos.html', context)
    pass


def loginView(request):
    
    if request.user.is_authenticated:
        # print('logueado')
        return render(request, 'Portal/home.html' )
    
    if request.method == 'POST':
            
        username=request.POST['username']
        password=request.POST['password']
        # print(username)
        user=authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            # print('autorizado')
            return render(request, 'Portal/home.html' )
        else:
            formulario_login = LoginForm()

            context = {
                'formulario_login': formulario_login,
                'messages':"Nombre o contraseña incorrectos"
            }
            return render(request, 'Portal/login.html',context)
    else:
        
        formulario_login = LoginForm()

    context = {
        'formulario_login': formulario_login,
    }

    return render(request, 'Portal/login.html', context)
    
    
def logoutView(request):
    
    logout(request)  
    return redirect('loginView')


@login_required    
def servicios(request):
    
    servicios=Servicio.objects.all()
    # print(servicios)
    context={'servicios': servicios}
    
    return render (request, 'Portal/mostrarServicios.html',context)

   
def listaDeImagenes():
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    listadoDeArchivos=os.listdir(os.path.join(BASE_DIR,'static/img'))
    listaImagenes=[]
    
    for archivo in listadoDeArchivos:
        
        modificado=archivo.replace('.jpg', '')
        modificado=modificado.replace('.JPG', '')
        listaImagenes.append(modificado)
     
    return listaImagenes    