from django.shortcuts import render, redirect
from django.conf import settings
from .forms import FormularioContacto
from Portal.models import *
# from django.views.generic.list import ListView
from Portal.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.urls import reverse
from Administrador.models import ListaDePrecios, PedidoPorMail, CatalogoSanitarios,CatalogoGas, CatalogoFerreteria, CatalogoBronce,CatalogoPPN, CatalogoThermofusion, CatalogoEpoxi, CatalogoSigas
from django.http import FileResponse
import os
from pathlib import Path
from django.db.models import Q
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponse
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

# @login_required
def lineas(request):
 
    lineas=Producto.objects.values_list('linea',flat=True).distinct().order_by('ordenLinea')
    # prioridad=ListaPrioritariaDeLineas.objects.values_list('archivo',flat=True)
    # print (lineas)  
    lineasConVersion=[]  
    for item in lineas:
        file_path = os.path.join(settings.MEDIA_ROOT,"img" , item+'.jpg')
        # print(file_path)
        version = int(os.path.getmtime(file_path)) if os.path.exists(file_path) else 0
        
        lineasConVersion.append((item, version))
        
         
    context={
            'lineas':lineas,
            'catalogos':listaDeCatalogos(),
            'MEDIA_URL': settings.MEDIA_URL,
            'lineasConVersion': lineasConVersion
             }
    # print(context)
    
    return render(request, 'Portal/mostrarLineas.html', context  )

def about(request):
    return render(request, 'Portal/about.html')

# @login_required
def seleccion(request,linea):   
         
        # lineas=Producto.objects.order_by().values_list('linea',flat=True).distinct()  
        rubro=Producto.objects.order_by('ordenRubro').values_list('rubro', flat=True).filter(linea=linea).distinct()
        # prioridad=ListaPrioritariaDeLineas.objects.values_list('archivo',flat=True)
        lineas=Producto.objects.values_list('linea',flat=True).distinct().order_by('ordenLinea')
        # print(rubro)
        imagenes=[]
        listaDeRubros=[]
        
        for item in rubro:
            # print(item)
            listaDeRubros.append(item)
            combo=[]
            imagen=Producto.objects.all().filter(rubro=item,linea=linea).first()
            # print(f'({imagen.imagen[:-1]})') 
            combo.append(imagen.imagen[:-1])   #le quito el salto de linea invisible al final ([:-1])
             
   
            file_path = os.path.join(settings.MEDIA_ROOT,"img" ,(imagen.imagen[:-1])+'.jpg')
            # print(file_path)
            version = int(os.path.getmtime(file_path)) if os.path.exists(file_path) else 0
            # print(version)
            combo.append(version)
            # print(combo)
            imagenes.append(combo)
                    
        diccionario=dict(zip(listaDeRubros,imagenes))   #la idea es pasar una lista dentro del archivo imagenes [imagen , version] EJ de diccionario:{'LLAVE DE GAS CAMPANAS': ['891100', 1693764694]}
        # print(diccionario)
        listadoDeImagenes=listaDeImagenes()
         
        context={
            'rubros':rubro,
            'diccionarios':diccionario,
            'listadoDeImagenes': listadoDeImagenes,
            'lineas':lineas,
            'linea':linea,
            'catalogos':listaDeCatalogos,
            'MEDIA_URL': settings.MEDIA_URL
            }
        return render(request,'Portal/mostrarRubros.html', context)
    
# @login_required    
def gondola(request,rubro,linea):
    
    # lineas=Producto.objects.order_by().values_list('linea',flat=True).distinct()  
    articulos=Producto.objects.all().filter(rubro=rubro, linea=linea).order_by('id')
    # prioridad=ListaPrioritariaDeLineas.objects.values_list('archivo',flat=True)
    lineas=Producto.objects.values_list('linea',flat=True).distinct().order_by('ordenLinea')
    
    for item in articulos:
        file_path = os.path.join(settings.MEDIA_ROOT,"img" ,(item.imagen[:-1])+'.jpg')
        version = int(os.path.getmtime(file_path)) if os.path.exists(file_path) else 0
        # print(f'archivo: {file_path} version: {version}')
        item.version=version
    
    
    context={
        'articulos':articulos,
        'lineas':lineas,
        'catalogos':listaDeCatalogos,
        'MEDIA_URL': settings.MEDIA_URL
        }
    # print(articulos)
    return render(request,'Portal/mostrarArticulos.html' ,context )

# @login_required
def portalSearch(request):
    
    if request.method =='GET':
        
        # lineas=Producto.objects.order_by().values_list('linea',flat=True).distinct() 
        # prioridad=ListaPrioritariaDeLineas.objects.values_list('archivo',flat=True)
        lineas=Producto.objects.values_list('linea',flat=True).distinct().order_by('ordenLinea')
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
        articulosOrdenados=articulos.order_by('cod_producto')
        context ={
            'articulos':articulosOrdenados,
            'lineas':lineas,
            'catalogos':listaDeCatalogos
            }
        print(articulos)
        return render(request,'Portal/mostrarArticulos.html', context)
    pass


def loginView(request):
    
    # if request.user.is_authenticated:
    #     # print('logueado')
    #     return redirect('lineas')
    
    # if request.method == 'POST':
            
    #     username=request.POST['username']
    #     password=request.POST['password']
    #     # print(username)
    #     user=authenticate(request, username=username, password=password)
        
    #     if user is not None:
    #         login(request,user)
    #         # print('autorizado')
    #         return redirect('lineas')
    #     else:
    #         formulario_login = LoginForm()

    #         context = {
    #             'formulario_login': formulario_login,
    #             'messages':"Nombre o contraseña incorrectos"
    #         }
    #         return render(request, 'Portal/login.html',context)
    # else:
        
    #     formulario_login = LoginForm()

    # context = {
    #     'formulario_login': formulario_login,
    # }

    return redirect('lineas')
    
    
def logoutView(request):
    
    logout(request)  
    return redirect('loginView')

def loginRedirect(request):
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
            
            messages.error(request,"Usuario o contraseña invalidos")
            return redirect('lineas')
    
    
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

def listaDeCatalogos():  #listas de precio y catálogos disponibles en el sistema
    BASE_DIR = Path(__file__).resolve().parent.parent
    listadoDeArchivos=os.listdir(os.path.join(BASE_DIR,'media/uploads'))
    
    listaDeCatalogos=[]
    for archivo in listadoDeArchivos:
        if archivo.startswith("Catalogo"):
            listaDeCatalogos.append(archivo)
        if archivo.startswith("ListaDePrecios"):
            listaDeCatalogos.append(archivo)
    return listaDeCatalogos 

def downloadLista(request):
    id=1
    obj=ListaDePrecios.objects.get(id=id)
    filename=obj.archivo.path
    # print(filename)
    response= FileResponse(open(filename,'rb'))
    return response

# def downloadPedidoPorMail(request):
#     id=1
#     obj=PedidoPorMail.objects.get(id=id)
#     filename=obj.archivo.path
#     response= FileResponse(open(filename,'rb'))
#     return response
def downloadPedidoPorMail(request):
    id=1
    obj=PedidoPorMail.objects.get(id=id)
    filename=obj.archivo.path
    res=open(filename,'rb') 
    response = HttpResponse(res, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Catalogo.pdf"'
    return response

def downloadCatalogo(request,nombre):
    if nombre.endswith('Sanitarios.pdf'):    
        id=1
        obj=CatalogoSanitarios.objects.get(id=id)
        filename=obj.archivo.path
        res=open(filename,'rb') 
        response = HttpResponse(res, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Sanitarios.pdf"'
        return response
    if nombre.endswith('Gas.pdf'):    
        id=1
        obj=CatalogoGas.objects.get(id=id)
        filename=obj.archivo.path
        res=open(filename,'rb') 
        response = HttpResponse(res, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Gas.pdf"'
        return response
    if nombre.endswith('Ferreteria.pdf'):    
        id=1
        obj=CatalogoFerreteria.objects.get(id=id)
        filename=obj.archivo.path
        res=open(filename,'rb') 
        response = HttpResponse(res, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Ferreteria.pdf"'
        return response
    if nombre.endswith('Bronce.pdf'):    
        id=1
        obj=CatalogoBronce.objects.get(id=id)
        filename=obj.archivo.path
        res=open(filename,'rb') 
        response = HttpResponse(res, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Bronce.pdf"'
        return response
    if nombre.endswith('PPN.pdf'):    
        id=1
        obj=CatalogoPPN.objects.get(id=id)
        filename=obj.archivo.path
        res=open(filename,'rb') 
        response = HttpResponse(res, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="PPN-Espiga.pdf"'
        return response 
    if nombre.endswith('Thermofusion.pdf'):    
        id=1
        obj=CatalogoThermofusion.objects.get(id=id)
        filename=obj.archivo.path
        res=open(filename,'rb') 
        response = HttpResponse(res, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Thermofusion.pdf"'
        return response 
    if nombre.endswith('Epoxi.pdf'):    
        id=1
        obj=CatalogoEpoxi.objects.get(id=id)
        filename=obj.archivo.path
        res=open(filename,'rb') 
        response = HttpResponse(res, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Epoxi.pdf"'
        return response
    if nombre.endswith('Sigas.pdf'):    
        id=1
        obj=CatalogoSigas.objects.get(id=id)
        filename=obj.archivo.path
        res=open(filename,'rb') 
        response = HttpResponse(res, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Sigas.pdf"'
        return response
    if nombre.endswith('ListaDePrecios.xlsx'):
        print("descargando lista de precios")
        id=1
        obj=ListaDePrecios.objects.get(id=id)
        filename=obj.archivo.path
        print("nombre del archivo" + filename)
        res=open(filename,'rb') 
        response = HttpResponse(res, content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; filename="ListaDePrecios.xlsx"'
        return response
        # return redirect('lineas')
    else:
        print ("Catalogo inexistente")    
def enviarPedidoDelCarrito(request):         # corrobora si el usuario exise y manda el pedido sino vuelve a lineas
    if request.method == "POST":
        
        username=request.POST['username']
        password=request.POST['password']
        # print(username)
       
        user=authenticate(request, username=username, password=password)
        # print(user)
       
        
        if user is not None:  #si esta autenticado envia el pedido
            
            textNombre = "Usuario: " + user.get_username()
            textMail ="Nro de Cliente: "+  user.get_email_field_name()
            textMensaje = 'Nombre: ' + request.POST['textMensaje']
            cuit='CUIT: ' + request.POST['cuit']
            telefono='Teléfono: ' + request.POST['telefono']
            direccion='Dirección: ' + request.POST['direccion']
            correo='Correo Electrónico: ' + request.POST['correo']
            expreso='Expreso: ' + request.POST['expreso']
            nota='Nota: ' + request.POST['nota']
            subject = 'Mail enviado desde el sitio de pedidos'
            
            key = request.COOKIES.get('carrito') #armo el mensaje desde las cookies del sitio 
            if len(key)>0:
                listaCarro=key.replace(",", "\n")
                message =listaCarro
                print(message)
            
                template =render_to_string('Portal/datos.html',{
                    'nombre':textNombre,
                    'email':textMail, #este es el correo de como estaba planeado el sistema de login antes
                    'message':message,
                    'telefono':telefono,
                    'direccion':direccion,
                    'correo':correo,  #este es el correo que ingresa el cliente
                    'mensaje':textMensaje,
                    'expreso':expreso,
                    'nota':nota,
                    'cuit':cuit
                })
                
                email=EmailMessage(
                    subject,
                    template,
                    settings.EMAIL_HOST_USER,
                    ['juanmazzocchi@gmail.com']    #OJO ESTO ES EL CORREO DE PRUEBA
                )
            
            try:
                
                email.fail_silently = False
                email.send()        
                messages.success(request, 'Email enviado correctamente.')
                return redirect('lineas')
            
            except:
                
                messages.error(request,'Algo salio mal')
                return redirect('lineas')
        else:
            messages.error(request,"Usuario o contraseña invalidos")
            return redirect('lineas')
             
        