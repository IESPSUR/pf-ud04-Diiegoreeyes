from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/listado', views.listado, name='listado'),
    path('tienda/crear', views.crear, name='crear'),
    path('tienda/editar', views.editar, name='editar'),
    path('eliminar/<int:id>', views.eliminar, name='eliminar'),
    path('tienda/editar/<int:id>', views.editar, name='editar'),

]
