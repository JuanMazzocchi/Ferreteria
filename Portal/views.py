from django.shortcuts import render, redirect
from django.conf import settings
from .forms import FormularioContacto
from Portal.models import *
# from django.views.generic.list import ListView
from Portal.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.urls import reverse
from Administrador.models import ListaDePrecios, PedidoPorMail,ListaPrioritariaDeLineas
from django.http import FileResponse
import os
from pathlib import Path
from django.db.models import Q
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from Ferreteria import settings



# @login_required
# def home(request):
                       
#     return render(request, 'Portal/home.html')

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
 
    lineas=Producto.objects.values_list('linea',flat=True).distinct().order_by('linea')
    prioridad=ListaPrioritariaDeLineas.objects.values_list('archivo',flat=True)
    context={
            'lineas':lineas,
             'prioridad':prioridad}
    # print(context)
    
    return render(request, 'Portal/mostrarLineas.html', context  )

def about(request):
    return render(request, 'Portal/about.html')

@login_required
def seleccion(request,linea):   
         
        lineas=Producto.objects.order_by().values_list('linea',flat=True).distinct()  
        rubro=Producto.objects.order_by('rubro').values_list('rubro', flat=True).distinct().filter(linea=linea)
        # print(rubro)
        imagenes=[]
        listaDeRubros=[]
        
        for item in rubro:
            # print(item)
            listaDeRubros.append(item)
            
            imagen=Producto.objects.all().filter(rubro=item)[0]
            print(f'({imagen.imagen[:-1]})') 
            imagenes.append(imagen.imagen[:-1])   #le quito el salto de linea invisible al final ([:-1])
        
        # print(imagenes)
        diccionario=dict(zip(listaDeRubros,imagenes))
        # print(diccionario)
        listadoDeImagenes=listaDeImagenes()
         
        context={
            'rubros':rubro,
            'diccionarios':diccionario,
            'listadoDeImagenes': listadoDeImagenes,
            'lineas':lineas
            }
        return render(request,'Portal/mostrarRubros.html', context)
    
@login_required    
def gondola(request,rubro):
    
    lineas=Producto.objects.order_by().values_list('linea',flat=True).distinct()  
    articulos=Producto.objects.all().filter(rubro=rubro).order_by('id')
    context={
        'articulos':articulos,
        'lineas':lineas
        }
    # print(articulos)
    return render(request,'Portal/mostrarArticulos.html' ,context )

@login_required
def portalSearch(request):
    
    if request.method =='GET':
        
        lineas=Producto.objects.order_by().values_list('linea',flat=True).distinct() 
        keyword=request.GET.get('keyword')
        # print(keyword)
        
        lista=keyword.split()
        
        query=Q()
        
        for palabra in lista:
            query &=Q(descripcion__icontains=palabra) 
        # print(query)         
        cod=Producto.objects.all().filter(cod_producto__contains=keyword)
        # linea=Producto.objects.all().filter(linea__icontains=keyword)
        # rubro=Producto.objects.all().filter(rubro__icontains=keyword)
        desc=Producto.objects.all().filter(query) 
        # articulos=cod.union(linea,rubro,desc)
        articulos=cod.union(desc)

        context ={
            'articulos':articulos,
            'lineas':lineas
            }
        # print(articulos)
        return render(request,'Portal/mostrarArticulos.html', context)
    pass


def loginView(request):
    
    if request.user.is_authenticated:
        # print('logueado')
        return redirect('lineas')
    
    if request.method == 'POST':
            
        username=request.POST['username']
        password=request.POST['password']
        # print(username)
        user=authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            # print('autorizado')
            return redirect('lineas')
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


# @login_required    
# def servicios(request):
    
#     servicios=Servicio.objects.all()
#     # print(servicios)
#     context={'servicios': servicios}
    
#     return render (request, 'Portal/mostrarServicios.html',context)

   
def listaDeImagenes():
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    listadoDeArchivos=os.listdir(os.path.join(BASE_DIR,'media/img'))
    listaImagenes=[]
    
    for archivo in listadoDeArchivos:
        
        modificado=archivo.replace('.jpg', '')
        modificado=modificado.replace('.JPG', '')
        listaImagenes.append(modificado)
     
    return listaImagenes    

def downloadLista(request):
    id=1
    obj=ListaDePrecios.objects.get(id=id)
    filename=obj.archivo.path
    print(filename)
    response= FileResponse(open(filename,'rb'))
    return response

def downloadPedidoPorMail(request):
    id=1
    obj=PedidoPorMail.objects.get(id=id)
    filename=obj.archivo.path
    response= FileResponse(open(filename,'rb'))
    return response


def enviarPedidoDelCarrito(request):
    
    if request.method =='POST':
        textNombre = "Enviado por: " + request.POST['textNombre']
        textMail ="Nro de Cliente: "+  request.POST['textMail']
        textMensaje = 'Mensaje: ' + request.POST['textMensaje']
        subject = 'Mail enviado desde el sitio de pedidos'
        
        key = request.COOKIES.get('carrito') #armo el mensaje desde las cookies del sitio 
        if len(key)>0:
            listaCarro=key.replace(",", "\n")
            message =listaCarro
        
            template =render_to_string('Portal/datos.html',{
                'nombre':textNombre,
                'email':textMail,
                'message':message,
                'mensaje':textMensaje,
            })
            
            email=EmailMessage(
                subject,
                template,
                settings.EMAIL_HOST_USER,
                ['juanmazzocchi@gmail.com']
            )
        
        try:
            
            email.fail_silently = False
            email.send()        
            messages.success(request, 'Email enviado correctamente.')
            return redirect('lineas')
        
        except:
            
            messages.error(request,'Algo salio mal')
            return redirect('lineas')
             
            
        
        
        