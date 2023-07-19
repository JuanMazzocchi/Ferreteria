from django.shortcuts import render
from Portal.models import *
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .forms import SearchForm, SearchServicioForm, SearchClienteForm
from .models import ArchivoCSV, ListaDePrecios
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

 

 

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
    
    
def BorrarBase(request):
    
    Producto.objects.all().delete()
    messages.success(request, 'Se borro la Base de datos')
    return render(request,'Administrador/abm.html')


def llenarBase(request):
    
    file=open('uploads/uploads/LISTPROVconPipecorregido.csv')
        
    for line in file:
        objeto= line.split(sep='|')
        # print(objeto)
                 
        if len(objeto)>=6:
            
            if objeto[0]=='cod producto':
                print(objeto[0])
                print(type(objeto[0]))
                pass
                    
            else:      
                precio=objeto[4].replace('.','')     
                            
                armado=Producto(cod_producto=objeto[0],
                                linea=objeto[1],
                                rubro=objeto[2],
                                descripcion=objeto[3],
                                pcio_lista=float(precio),
                                unidad=objeto[5],
                                imagen=objeto[6] )
                    
                try:
                    armado.save()
                    
                except armado.save():
                    messages.error(request,"Algo salio mal")
                    return render(request,'Administrador/abm.html')
    
    messages.success(request, 'Se persistio la Base de datos')
    return render(request,'Administrador/abm.html')
    
class SubirListaDePreciosView(SuccessMessageMixin, CreateView):
        
    model=ListaDePrecios
    fields='__all__'
    success_url='abm'
    success_message='Lista de Precios subida correctamente'
    template_name='Administrador/subirListaDePrecios.html'
    
 
    
def ListasDePrecio(request):
    
    obj=ListaDePrecios.objects.all()
    context={'listas':obj}
    print(context)
    return render(request, 'Administrador/listasResultadosSearch.html', context)
    