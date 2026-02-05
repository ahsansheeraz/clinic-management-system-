from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

     
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
]
