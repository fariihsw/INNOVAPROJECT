
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import configuracion, login_view, logout_view, eliminar

urlpatterns = [
    path('lista/', views.lista, name="lista"),
    path('agregar/', views.agregar, name="agregar"),
    path('actualizar/', views.actualizar, name="actualizar"),
    path('configuracion/', configuracion, name='configuracion'),
    path('eliminar/', eliminar, name='eliminar'),
    #path('eliminar/', views.eliminar, name="eliminar"),
    path('indicador/', views.indicador, name="indicador"),
    path('alertas/', views.alertas, name="alertas"),
    path('registro/', views.registro, name="registro"),
    path('notifica/', views.notifica, name="notifica"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('get_chart/', views.get_chart, name="get_Chart"),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('accounts/login/', login_view, name='login'),

   # path('accounts/', include('django.contrib.auth.urls')), 
 # Para login, logout, etc.
    
    #path('login', views.loginn, name="paginalogin"),
    # Puedes añadir otras URLs que necesites aquí.
]



#urlpatterns = [
    
#    path('', views.index, name= "index"),
#    path('lista', views.lista, name= "lista"),
#    path('agregar', views.agregar, name= "agregar"),
#    path('actualizar', views.actualizar, name= "actualizar"),
#    path('eliminar', views.eliminar, name= "eliminar"),
#    path('indicador', views.indicador, name= "indicador"),
#    path('alertas', views.alertas, name= "alertas"),
#    path('notifica', views.notifica, name= "notifica"),
#    #path('login_admin', views.login_admin, name= "login_admin"),
#    path('login', login_view, name="login"),
    # mi_aplicacion/urls.py
  #  path('login' , views.login, name= "login" ),
#    path('accounts/', include ('django.contrib.auth.urls')),
   # path('signin' , views.signin, name= "signin" ),
#]

#from django.contrib import admin
#from django.urls import path
#from django import views

#from django.contrib.auth import views
#from . import views
#from django.urls import path, include
#from .views import login
#from .views import login_view