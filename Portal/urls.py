from django.urls import path, re_path, include
from . import views

urlpatterns = [
path('',views.loginView, name='loginView'),
path('inicio',views.home , name='inicio'),
path('contacto',views.contacto, name='contacto'),
path('about', views.about, name="about"),
path('lineas',views.lineas, name='lineas'),
path('seleccion/<str:linea>',views.seleccion , name='seleccion'),
path('gondola/<path:rubro>', views.gondola , name='gondola'),
path('portalSearch', views.portalSearch, name='portalSearch'),
path('logout',views.logoutView, name='logout'),
path('servicios',views.servicios, name='servicios'),
path('listaDeImagenes',views.listaDeImagenes, name='listaDeImagenes'),
 
 
]
