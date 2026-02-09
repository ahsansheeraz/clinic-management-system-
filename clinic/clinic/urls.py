 
from django.contrib import admin
from django.urls import path, include
 

urlpatterns = [
     
    path('admin/', admin.site.urls),
    
    path('users/', include('users.urls')),
    
    path('doctor/', include('doctor.urls', namespace='doctor')),
    path('patients/', include('patients.urls', namespace='patients')),

 
]
