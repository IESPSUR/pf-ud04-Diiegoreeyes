from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/admin/listado', views.listado, name='listado'),
    path('tienda/admin/crear', views.crear, name='crear'),
    path('tienda/admin/editar', views.editar, name='editar'),
    path('eliminar/admin/<int:id>', views.eliminar, name='eliminar'),
    path('tienda/admin/editar/<int:id>', views.editar, name='editar'),

]
