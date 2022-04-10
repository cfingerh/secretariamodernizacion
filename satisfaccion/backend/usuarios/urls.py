from django.conf.urls import url
from django.urls import path, re_path
from rest_framework import routers
# from usuarios.api.usuario_actual import UserView
# from usuarios.api.gestor_usuario import UserView as GestorUserView
from usuarios import views

router = routers.SimpleRouter()

# router.register(r'api/usuario_actual', UserView, 'usuario_actual')
# router.register(r'api/crear_usuario', GestorUserView, 'crear_usuario')
# router.register(r'api/listar_intrumentos', InstrumentoView, 'listar_intrumentos')
# router.register(r'api/listar_subdirecciones', SubdireccionView, 'listar_subdirecciones')
# router.register(r'api/listar_agencias', AgenciaView, 'listar_agencias')

urlpatterns = [
    url(r'^info/$', views.info),
    url(r'^register/$', views.register),
    url(r'^agregar/$', views.agregar),
    url(r'^eliminar/$', views.eliminar),
    path('getPerfiles/<int:service_id>/', views.getPerfiles),
    path('claveunica/', views.claveunica),
    path('login_with_hash/', views.login_with_hash),
    path('is_user/', views.is_user),
    path('change_modulos/<int:serviceuser_id>/', views.change_modulos),
]

urlpatterns += router.urls
