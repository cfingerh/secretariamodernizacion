from datetime import datetime

from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import JsonResponse

from django_filters import rest_framework as filters

from portal.models import Carga


class GeneralPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        # if view.action in ['instituciones']:
        #     return True

        if view.action in ['list', 'retrieve', 'aprobar', 'rechazar', 'eliminar']:
            return request.user.is_authenticated
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_superuser

        return False


class Filter(filters.FilterSet):

    class Meta:
        model = Carga
        fields = {
            'institucion': ['exact'],
        }


class Serializer(serializers.ModelSerializer):

    class Meta:
        model = Carga
        fields = ('id',
                  'status',
                  'data',
                  'historial'

                  )


class ViewSet(viewsets.ModelViewSet):
    queryset = Carga.objects.all().order_by('id')
    serializer_class = Serializer
    permission_classes = [IsAuthenticated, GeneralPermission]
    filter_class = Filter

    def get_queryset(self):
        queryset = self.queryset.exclude(status='eliminado')  # .filter(pk__in=self.request.user.service_set.all().values('ministry_id'))
        return queryset

    @action(detail=True, methods=['post'])
    def aprobar(self, request, *args, **kwargs):
        carga = self.get_object()

        # TODO: permisos, consierar que Dato es distinot a presentación

        # if status_de == 'elaboracion':
        #     if 'encargado' not in tipos:
        #         raise serializers.ValidationError('No autorizado')
        #     status_a = 'revision_jefe_servicio'

        log = {
            'de': carga.status,
            'a': 'aprobado',
            'user': {'id': request.user.id,
                     'nombre_completo': request.user.get_nombre_completo,
                     'username': request.user.username},
            'fechahora': str(datetime.now()),
        }

        carga.status = 'aprobado'
        historial = carga.historial
        logs = historial.get("logs") or []
        logs.append(log)
        historial["logs"] = logs
        carga.historial = historial
        carga.save()
        serializer = self.get_serializer(carga)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def rechazar(self, request, *args, **kwargs):
        carga = self.get_object()

        # TODO: permisos, consierar que Dato es distinot a presentación

        # if status_de == 'elaboracion':
        #     if 'encargado' not in tipos:
        #         raise serializers.ValidationError('No autorizado')
        #     status_a = 'revision_jefe_servicio'

        log = {
            'de': carga.status,
            'a': 'rechazado',
            'user': {'id': request.user.id,
                     'nombre_completo': request.user.get_nombre_completo,
                     'username': request.user.username},
            'fechahora': str(datetime.now()),
        }

        carga.status = 'rechazado'
        historial = carga.historial
        logs = historial.get("logs") or []
        logs.append(log)
        historial["logs"] = logs
        carga.historial = historial
        carga.save()
        serializer = self.get_serializer(carga)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def eliminar(self, request, *args, **kwargs):
        carga = self.get_object()

        log = {
            'de': carga.status,
            'a': 'eliminado',
            'user': {'id': request.user.id,
                     'nombre_completo': request.user.get_nombre_completo,
                     'username': request.user.username},
            'fechahora': str(datetime.now()),
        }

        carga.status = 'eliminado'
        historial = carga.historial
        logs = historial.get("logs") or []
        logs.append(log)
        historial["logs"] = logs
        carga.historial = historial
        carga.save()
        serializer = self.get_serializer(carga)
        return Response(serializer.data)


from django.http import JsonResponse
