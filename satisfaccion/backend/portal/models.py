from django.db import models
from django.contrib.postgres.fields import JSONField

from usuarios.models import User


class Carga(models.Model):
    institucion = models.ForeignKey('base.Institucion', models.DO_NOTHING, related_name='cargas')
    status = models.CharField(blank=True, null=True, max_length=255, )
    historial = JSONField(default=dict)
    data = JSONField(default=dict)


class Permiso(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    institucion = models.ForeignKey('base.Institucion', models.DO_NOTHING, related_name='permisos')
    tipo = models.CharField(blank=True, null=True, max_length=255, )  # servicio, empresa
