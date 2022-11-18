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
    path('tienda/formcompra/<int:id>', views.formcompra, name='formcompra'),
    path('tienda/listacompra',views.listacompra, name='listacompra'),
    path('tienda/crearusuario', views.crearusuario, name='crearusuario'),
    path('tienda/iniciar_sesion', views.iniciar_sesion, name='iniciar_sesion'),
    path('tienda/informes', views.informes, name='informes'),
    path('tienda/informes/listado_marca', views.listado_marca, name='listado_marca'),
    path('tienda/informes/listado_usuario', views.listado_usuario, name='listado_usuario'),
    path('tienda/informes/toptenproductos', views.toptenproductos, name='toptenproductos'),
    path('tienda/informes/toptenclientes', views.toptenclientes, name='toptenclientes'),


]
