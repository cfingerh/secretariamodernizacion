from rest_framework import routers
from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from base.api import instituciones
from base import views

router = routers.SimpleRouter()

router.register(r'instituciones', instituciones.View,)


urlpatterns = [

    path('data_grafica/', views.data_grafica),
    path('data_grafica/<str:pk>', views.data_grafica),
    path('data_dimension/', views.data_dimension),
    path('data_dimension/<str:pk>', views.data_dimension),
    path('data_dimension_anio/', views.data_dimension_anio),
    path('data_dimension_anio/<str:pk>', views.data_dimension_anio),
    path('data_imagen/', views.data_imagen),
    path('data_imagen/<str:pk>', views.data_imagen),
    path('data_atributos/', views.data_atributos),
    path('data_atributos/<str:pk>', views.data_atributos),
    path('canal_evaluacion/', views.canal_evaluacion),
    path('canal_evaluacion/<str:pk>', views.canal_evaluacion),
    path('canal_preferencia/', views.canal_preferencia),
    path('canal_preferencia/<str:pk>', views.canal_preferencia),
    path('informe/<str:codigo_dipres>', views.informe),

    path('resumen/', views.resumen)
]


urlpatterns += router.urls
