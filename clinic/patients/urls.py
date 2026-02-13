from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('add/', views.patient_add, name='patient_add'),
    path('edit/<int:pk>/', views.patient_edit, name='patient_edit'),
    path('delete/<int:pk>/', views.patient_delete, name='patient_delete'),
]
