from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from .api import cargas
from . import views

router = routers.SimpleRouter()
# router.register(r'', services.ViewSet)
router.register(r'cargas', cargas.ViewSet)

urlpatterns = [
    path('excel/', views.excel),
    path('instituciones/', views.instituciones),
    # path('prueba/', views.prueba),

    path('subir/<int:institucion_id>/', views.subir),
    path('carga/pdf_dato/<int:carga_id>/', views.pdf_dato),
    path('carga/pdf_presentacion/<int:carga_id>/', views.pdf_presentacion),
    path('carga/evaluar/<int:carga_id>/', views.evaluar),
    path('carga/descarga/<int:carga_id>/', views.descarga),

]

urlpatterns += router.urls
