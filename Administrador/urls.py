from django.urls import path, re_path, include
from . import views

urlpatterns = [
path('abm',views.abm , name='abm'),
# path('productosView' , views.ProductoListView.as_view(), name='ProductosView'),
path('productoCreateView',views.ProductoCreateView.as_view(), name='ProductoCreateView'),
path('search',views.search, name='search'),
path('productosEditar/<int:pk>', views.ProductoUpdateView.as_view(), name='productosEditar'),
path('productosEliminar/<int:pk>', views.ProductoEliminarView.as_view(),name='productosEliminar'),

# path('servicioCreateView', views.ServicioCreateView.as_view(), name='ServicioCreateView'),
# path('servicioSearch', views.servicioSearch, name='servicioSearch'),
# path('servicioEditar/<int:pk>',views.ServicioUpdateView.as_view(), name='servicioEditar'),
# path('servicioEliminar/<int:pk>', views.ServicioEliminarView.as_view(),name='servicioEliminar'),

# path('clienteCreateView', views.ClienteCreateView.as_view(), name='clienteCreateView'),
# path('clienteSearch',views.clienteSearch, name='clienteSearch'),
# path('clienteEditar/<int:pk>', views.ClienteUpdateView.as_view(), name='clienteEditar'),
# path('clienteEliminar/<int:pk>', views.ClienteEliminarView.as_view(), name='clienteEliminar'),

path('subirCsv',views.SubirCsvView.as_view(), name='subirCsv'),
path('borrarBase',views.BorrarBase, name='borrarBase'),
path('llenarBase', views.llenarBase, name='llenarBase'),

path('subirLista',views.SubirListaDePreciosView.as_view(), name='subirLista'),
path('listasDePrecio',views.ListasDePrecio, name='listasDePrecio'),
path('subirFoto',views.FotoCreateView.as_view(), name='subirFoto'),
path('subirPedidoPorMail', views.PedidoPorMailCreateView.as_view(), name='subirPedidoPorMail')
 
 
]