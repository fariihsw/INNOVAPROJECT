
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('panel.urls')),
    #path('api/', include('api.urls'))  
    #path('accounts/', include('django.contrib.auth.urls')),
    
   # path('innovarpa/', include('innovarpa.urls')),
 
    ]