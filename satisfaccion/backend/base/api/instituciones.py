from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action


from django_filters import FilterSet
from django.http import JsonResponse

from base.models import Institucion

from rest_framework import serializers
from django.shortcuts import get_object_or_404

import boto3
import os


BUCKET = os.environ["BUCKET"]
BUCKET_HTTP = os.environ["BUCKET_HTTP"]
S3 = boto3.resource('s3', aws_access_key_id=os.environ["CLAVE_AWS_ACCESS_KEY_ID"],
                    aws_secret_access_key=os.environ["CLAVE_AWS_SECRET_ACCESS_KEY"])


class Filter(FilterSet):

    class Meta:
        model = Institucion
        fields = {
            'nombre': ['exact'],
        }


class Serializer(serializers.ModelSerializer):

    class Meta:
        model = Institucion
        fields = ('id',
                  'nombre_a_mostrar',
                  'nombre_corto',
                  'resumen',
                  'datos')


class View(viewsets.ModelViewSet):

    queryset = Institucion.objects.filter().order_by('nombre')
    serializer_class = Serializer
    permission_classes = (AllowAny,)
    filter_class = Filter

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            return queryset.get(datos__codigo_dipres__iexact=self.kwargs[lookup_url_kwarg])
        except:
            pass
        obj = get_object_or_404(queryset, **filter_kwargs)

        return obj

    @action(detail=True, methods=['get'])
    def ultimo_informe(self, request, pk):
        instance = self.get_object()
        codigo_dipres = instance.datos.get("codigo_dipres")
        my_bucket = S3.Bucket(BUCKET)

        for object_summary in my_bucket.objects.filter(Prefix="ultimo_informe/"):
            if object_summary.key.split("/")[-1].split("_")[0] == codigo_dipres:
                url = '{}/{}'.format(BUCKET_HTTP, object_summary.key)
                return JsonResponse({'url': url})

        return JsonResponse({}, status=500)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        buscar = request.GET.get("buscar")
        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_grupo(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        grupos = []
        for grupo in queryset.distinct('datos__agrupacion').order_by('datos__agrupacion').values('datos__agrupacion'):
            instituciones = []
            instituciones_q = queryset.exclude().filter(datos__agrupacion=grupo.get("datos__agrupacion")).order_by('nombre')
            for institucion in instituciones_q:
                instituciones.append({'nombre': institucion.nombre if institucion.nombre and len(institucion.nombre) > 0 else institucion.datos.get("codigo"),
                                      'codigo': institucion.datos.get("codigo"),
                                      'codigo_dipres': institucion.datos.get("codigo_dipres"),
                                      'id': institucion.id})
            grupos.append({'nombre': grupo.get("datos__agrupacion", 'SinNombre'), 'instituciones': instituciones})

        return JsonResponse(grupos, safe=False)
