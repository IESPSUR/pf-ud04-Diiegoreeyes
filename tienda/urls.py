from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/informe/', views.informe, name='informe'),
    path('tienda/actualizar/', views.informe, name='actualizar'),
]