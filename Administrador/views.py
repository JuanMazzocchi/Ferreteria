from django.shortcuts import render, redirect
from Portal.models import *
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .forms import SearchForm, SearchServicioForm, SearchClienteForm
from .models import ArchivoCSV, ListaDePrecios, FotosDeProductos, PedidoPorMail, ListaPrioritariaDeLineas
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from Ferreteria import settings
import os


 

# Create your views here.
def abm(request):
    return render(request,'Administrador/abm.html')

class ProductoListView(ListView):
    model = Producto                #no esta en funcionamiento
    paginate_by=50
    template_name='Administrador/productoListView.html'
    

class ProductoCreateView(SuccessMessageMixin, CreateView):
    model = Producto
    template_name ='Administrador/productoCreateView.html'
    fields='__all__'
    success_message='Producto creado satisfactoriamente'
    success_url=reverse_lazy('abm')
   
class ProductoUpdateView(SuccessMessageMixin, UpdateView):
    model=Producto
    fields='__all__'
    success_url=reverse_lazy('abm')
    success_message='Producto editado Correctamente'
    template_name='Administrador/productoUpdateForm.html'
    
    
class ProductoEliminarView(DeleteView):
    model=Producto
    template_name='Administrador/productoEliminar.html'
    success_message='Producto Eliminado satisfactoriamente'
    success_url=reverse_lazy('abm')  



def search(request):
    
    if request.method == 'POST':
        busqueda=SearchForm(request.POST)
           
        if busqueda.is_valid():
            keyword=busqueda.cleaned_data['keyword']
        
            cod=Producto.objects.all().filter(cod_producto__contains=keyword)
            linea=Producto.objects.all().filter(linea__icontains=keyword)
            rubro=Producto.objects.all().filter(rubro__icontains=keyword)
            desc=Producto.objects.all().filter(descripcion__icontains=keyword)
            articulos=cod.union(linea,rubro,desc)
            for e in articulos:
                # print(e.imagen[:-1])
                e.imagen=e.imagen[:-1] # le quito el salto de linea invisible
            context ={'articulos':articulos }
            return render(request,'Administrador/ResultadosSearch.html', context)
    else:
        busqueda=SearchForm()    
    
    return render(request,'Administrador/productoSearch.html', {'busqueda' : busqueda})
        
# class ServicioCreateView(SuccessMessageMixin, CreateView):
#     model = Servicio
#     template_name ='Administrador/servicioCreateView.html'
#     fields='__all__'
#     success_message='Servicio creado satisfactoriamente'
#     success_url=reverse_lazy('abm') 
        

# class ServicioUpdateView(SuccessMessageMixin, UpdateView):
#     model=Servicio
#     fields='__all__'
#     success_url=reverse_lazy('abm')
#     success_message='Servicio editado Correctamente'
#     template_name='Administrador/servicioUpdateForm.html'
    
# def servicioSearch(request):
    
#     if request.method == 'POST':
#         busqueda=SearchServicioForm(request.POST)
           
#         if busqueda.is_valid():
#             keyword=busqueda.cleaned_data['keyword']
        
             
#             desc=Servicio.objects.all().filter(descripcion__icontains=keyword)
                     
#             context ={'articulos':desc }
#             return render(request,'Administrador/serviciosResultadosSearch.html', context)
#     else:
#         busqueda=SearchServicioForm()    
    
#     return render(request,'Administrador/servicioSearch.html', {'busqueda' : busqueda})

# class ServicioEliminarView(SuccessMessageMixin, DeleteView):
#     model=Servicio
#     template_name='Administrador/servicioEliminar.html'
#     success_message='Servicio Eliminado satisfactoriamente'
#     success_url=reverse_lazy('abm')  
    
    
# class ClienteCreateView(SuccessMessageMixin, CreateView):
#     model=Cliente
#     template_name='Administrador/clienteCreateView.html'
#     fields='__all__'
#     success_message='Cliente creado correctamente'
#     success_url=reverse_lazy('abm')
    
# def clienteSearch(request):
#     if request.method == 'POST':
#         busqueda=SearchClienteForm(request.POST)
           
#         if busqueda.is_valid():
#             keyword=busqueda.cleaned_data['keyword']
        
             
#             nom=Cliente.objects.all().filter(nombre__icontains=keyword)
#             apell=Cliente.objects.all().filter(apellido__icontains=keyword)
#             resultados=nom.union(apell)
#             context ={'articulos':resultados }
#             return render(request,'Administrador/clienteResultadosSearch.html', context)
#     else:
#         busqueda=SearchServicioForm()    
    
#     return render(request,'Administrador/clienteSearch.html', {'busqueda' : busqueda})
    
    
# class ClienteUpdateView(SuccessMessageMixin, UpdateView):
#     model=Cliente
#     fields='__all__'
#     success_url='abm'
#     success_message='Cliente editado correctamente'
#     template_name='Administrador/clienteUpdateForm.html'
    
# class ClienteEliminarView(SuccessMessageMixin, DeleteView):
#     model=Cliente
#     template_name='Administrador/clienteEliminar.html'
#     success_message='Cliente Eliminado satisfactoriamente'
#     success_url=reverse_lazy('abm') 
 
class SubirCsvView(SuccessMessageMixin, CreateView):
    
    model=ArchivoCSV
    fields='__all__'
    success_url='abm'
    success_message='Archivo subido correctamente'
    template_name='Administrador/subirCSV.html'

# def upload_csv(request):
    
#     if request.method =="GET":
#         return render (request,'Administrador/upload_csv.html')          #SIN USO, LO USE COMO PRUEBA PERO EN PRODUCCION NO FUNCIONA BIEN
    
#     try:
#        csv_file = request.FILES["csv_file"]
#        if not csv_file.name.endswith('.csv'):
#            messages.error(request, 'El archivo no es .csv')
#            return (request,'Administrador/abm.html') 
       
#        file_data= csv_file.read().decode('ISO-8859-1')
#        #BorrarBase(request)
#        lines = file_data.split('\n')
#     #    print(lines[0])
#        for line in lines:
#            objeto=line.split("|")
#            if len(objeto)>=6:
                
#             if objeto[0]=='cod producto':
#                 # print(objeto[0])
#                 # print(type(objeto[0]))
#                 pass
                    
#             else:      
#                 # precio=objeto[4].replace('.','')     
#                 precio=objeto[4] 
#                 armado=Producto(cod_producto=objeto[0],
#                                 linea=objeto[1],
#                                 rubro=objeto[2],
#                                 descripcion=objeto[3],
#                                 pcio_lista=float(precio),
#                                 unidad=objeto[5],
#                                 imagen=objeto[6] )
                    
#                 try:
#                     armado.save()
                    
#                 except Exception as e :
#                     messages.error(request,"Algo saio mal  "+repr(e))
#                     return render(request,'Administrador/abm.html')
    
#     except Exception as e :
#         messages.error(request,"Unable to upload file. "+repr(e))

    
           
           
#     messages.success(request, 'Se persistio la Base de datos desde el archivo .csv')
#     return render(request,'Administrador/abm.html')       
                
     
    
    
 




def BorrarLlenar(request):
    
    BorrarBase(request)
    # llenarBase(request) 
    worker().start()            #asi llena la base sin parar el sitio
    return redirect('abm')
    
def BorrarBase(request):
    
    Producto.objects.all().delete()
    messages.success(request, 'Se borro la Base de datos')
    return render(request,'Administrador/abm.html')


 
from chardet import detect

# get file encoding type
def get_encoding_type(file):
    print("@@@@")
    with open(file, 'rb') as f:
        rawdata = f.read()
    print(detect(rawdata)['encoding'])
    return detect(rawdata)['encoding']


import time


# def llenarBase(request):
            
#     path=os.path.join(settings.MEDIA_DIR, 'uploads/BaseDeDatos.csv')      # SIN USO, EN PRODUCCION NO FUNCIONA BIEN
    
#     try:
#         file=open(path, 'r', encoding=get_encoding_type(path) , errors='ignore')
        
#     except:
#         messages.error(request,"No se pudo abrir el archivo .csv")
#         return render(request,'Administrador/abm.html')
#     # contador=0
#     for line in file:
#         objeto= line.split(sep='|')
#         print(objeto)
        
#         # if contador %2000 ==0:
#         #     print(f"esperando  {time.time()}")
#         #     time.sleep(10)
                 
#         if len(objeto)>=6:
            
#             if objeto[0]=='cod producto':
#                 # print(objeto[0])
#                 # print(type(objeto[0]))
#                 pass
                    
#             else:      #orden en el archivo CSV : cod_producto, linea, ordenLinea, rubro , ordenRubro, descripcion, pcio_lista, unidad, imagen 
#                 # precio=objeto[4].replace('.','')     
                 
#                 precio=objeto[6] 
#                 armado=Producto(cod_producto=objeto[0],
#                                 linea=objeto[1],
#                                 ordenLinea=objeto[2],
#                                 rubro=objeto[3],
#                                 ordenRubro=objeto[4],
#                                 descripcion=objeto[5],
#                                 pcio_lista=float(precio),
#                                 unidad=objeto[7],
#                                 imagen=objeto[8] )
                    
#                 try:
#                     armado.save()
#                     # contador+=1
                    
#                 except armado.save():
#                     print(objeto)
#                     messages.error(request,"Algo salio mal")
#                     return render(request,'Administrador/abm.html')
                
    
#     messages.success(request, 'Se persistio la Base de datos desde el archivo .csv')
#     return render(request,'Administrador/abm.html')

from threading import Thread

class worker(Thread):
    def run(self):
                  
         path=os.path.join(settings.MEDIA_DIR, 'uploads/BaseDeDatos.csv')
         file=open(path, 'r', encoding=('ISO-8859-1') , errors='ignore')
         for line in file:
             objeto= line.split(sep='|')
            #  print(objeto)
             if len(objeto)>=6:
                if objeto[0]=='cod producto':
                     pass
                    
                else:
                    precio=objeto[6] 
                    armado=Producto(cod_producto=objeto[0].strip(),
                                linea=objeto[1].strip(),
                                ordenLinea=objeto[2].strip(),
                                rubro=objeto[3].strip(),
                                ordenRubro=objeto[4].strip(),
                                descripcion=objeto[5].strip(),
                                pcio_lista=float(precio),
                                unidad=objeto[7].strip(),
                                imagen=objeto[8])
                        
                    try:
                        armado.save()
                                            
                    except armado.save():
                        print('error salvando fila en la db')


def baseDeDatos(request):
    return render(request,'Administrador/baseDeDatos.html')
    
class SubirListaDePreciosView(SuccessMessageMixin, CreateView):
        
    model=ListaDePrecios
    fields='__all__'
    success_url='abm'
    success_message='Lista de Precios subida correctamente'
    template_name='Administrador/subirListaDePrecios.html'
    
 
    
def ListasDePrecio(request):
    
    obj=ListaDePrecios.objects.all()
    context={'listas':obj}
    # print(context)
    return render(request, 'Administrador/listasResultadosSearch.html', context)
    
    
class FotoCreateView(SuccessMessageMixin, CreateView):
    model = FotosDeProductos
    template_name ='Administrador/fotoCreateView.html'
    fields=['archivo']
    success_message='Foto subida correctamente'
    success_url=reverse_lazy('abm')
    
class PedidoPorMailCreateView(SuccessMessageMixin, CreateView):
    model = PedidoPorMail
    template_name ='Administrador/subirPedidoPorMail.html'
    fields=['archivo']
    success_message='Archivo subido correctamente'
    success_url=reverse_lazy('abm')
 
    
def prioridad(request):
    lineas=Producto.objects.values_list('linea',flat=True).distinct().order_by('linea')
    context={'lineas':lineas}
    # print(context)
    return render(request,'Administrador/prioridadLineas.html',context)

def confirmaPrioridad(request):   #ya no esta en uso
    if request.method == "POST":
        primer=request.POST.get('casilla1') 
        segunda=request.POST.get('casilla2')
        tercera=request.POST.get('casilla3')
        cuarta=request.POST.get('casilla4')
        quinta=request.POST.get('casilla5')
        sexta=request.POST.get('casilla6')
        septima=request.POST.get('casilla7')
        octava=request.POST.get('casilla8')
        # print('*****')
        # print(primer,segunda,tercera,cuarta,quinta,sexta,septima,octava)
        lista=[primer,segunda,tercera,cuarta,quinta,sexta,septima,octava] 
        ListaPrioritariaDeLineas.objects.all().delete()
        # nuevalista=ListaPrioritariaDeLineas(1,lista)
        # nuevalista.save()
        index=1
        for item in lista:
             
            ListaPrioritariaDeLineas(index,item).save()
            index+=1
            
        messages.success(request,'Se actualizo correctamente la lista de prioridades')
        return render(request,'Administrador/abm.html')
    else:
        return render(request,'Administrador/prioridadLineas.html')