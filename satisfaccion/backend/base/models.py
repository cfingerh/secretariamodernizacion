from django.db import models
from datetime import datetime


class Institucion(models.Model):
    nombre = models.TextField()  # noimbre para relación con Menu
    codigo_dipres = models.TextField(null=True, blank=True)
    nombre_corto = models.TextField(null=True, blank=True)

    otros_nombres = models.TextField(null=True, blank=True)  # el mismo que context tittulo
    datos = models.JSONField(default=dict)
    resumen = models.JSONField(default=dict)

    def nombre_a_mostrar(self):
        return self.nombre or self.datos.get("codigo")

    def calcular_resumen(self):
        from base.views import get_valores
        if self.datos.get("anios") is None or len(self.datos.get("anios")) == 0:
            return {'anios': None, 'ultimo': None, 'canales': None}

        res = []
        satisfaciones = []
        for anio in self.datos.get("anios"):
            res.append({
                'anio': anio,
                'eval_inst': get_valores(self.respuesta_set.filter(anio=anio), 'eval_inst'),
                'experiencia': get_valores(self.respuesta_set.filter(anio=anio), 'experiencia')}
            )
            satisfaciones.append(get_valores(self.respuesta_set.filter(anio=anio), 'experiencia')["positivo"])

        anio = 2020
        canales = {
            'Callcenter': get_valores(self.respuesta_set.filter(anio=anio), 'pec_eval_telefono'),
            'Web': get_valores(self.respuesta_set.filter(anio=anio), 'pec_eval_web'),
            'Oficinas': get_valores(self.respuesta_set.filter(anio=anio), 'pec_eval_presencial')}

        return {'anios': res,
                'ultimo': res[-1],
                'canales': canales,
                'satisfaction_neta': satisfaciones[-1],
                'satisfaciones': satisfaciones}

# class Dato(models.Model):
#     anio = models.IntegerField()
#     institucion = models.ForeignKey(Institucion, on_delete=models.SET_NULL, null=True)
#     datos = models.JSONField(default=dict)


class Raw(models.Model):
    # TBD
    codigo_cf = models.TextField(db_index=True, null=True, blank=True)  # noimbre para relación con Menu

    institucion = models.ForeignKey(Institucion, on_delete=models.SET_NULL, null=True)

    anio = models.TextField(db_index=True, null=True, blank=True)  # el mismo que context tittulo
    datos = models.JSONField(default=dict)
    especial = models.TextField(db_index=True, null=True, blank=True)


class Respuesta(models.Model):
    anio = models.IntegerField(null=True, blank=True, db_index=True)
    f_pond = models.FloatField(null=True, blank=True)
    experiencia = models.IntegerField(null=True, blank=True, db_index=True)
    eval_inst = models.IntegerField(null=True, blank=True, db_index=True)
    edad = models.TextField(null=True, blank=True, db_index=True)
    sexo = models.TextField(null=True, blank=True, db_index=True)
    educacion = models.TextField(null=True, blank=True, db_index=True)
    habilitado = models.TextField(null=True, blank=True, db_index=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.SET_NULL, null=True)

    tipo_tramite = models.TextField(null=True, blank=True, db_index=True)
    tuvo_problema = models.TextField(null=True, blank=True, db_index=True)

    especial = models.TextField(db_index=True, null=True, blank=True)
    region = models.TextField(db_index=True, null=True, blank=True)

    # Imagen
    pi_imagen_confianza = models.IntegerField(null=True, blank=True, db_index=True)
    pi_imagen_transp = models.IntegerField(null=True, blank=True, db_index=True)
    pi_imagen_preocupa = models.IntegerField(null=True, blank=True, db_index=True)
    pi_imagen_actual = models.IntegerField(null=True, blank=True, db_index=True)
    pi_imagen_funcion = models.IntegerField(null=True, blank=True, db_index=True)
    pi_imagen_satisface = models.IntegerField(null=True, blank=True, db_index=True)

    pec_eval_telefono = models.IntegerField(null=True, blank=True, db_index=True)
    pec_eval_web = models.IntegerField(null=True, blank=True, db_index=True)
    pec_eval_presencial = models.IntegerField(null=True, blank=True, db_index=True)

    pec_canal_telefono = models.IntegerField(null=True, blank=True, db_index=True)
    pec_canal_web = models.IntegerField(null=True, blank=True, db_index=True)
    pec_canal_presencial = models.IntegerField(null=True, blank=True, db_index=True)

    # atributos
    pev_tram_facil = models.IntegerField(null=True, blank=True, db_index=True)
    pev_tram_tiempo = models.IntegerField(null=True, blank=True, db_index=True)
    pev_tram_claridad_pasos = models.IntegerField(null=True, blank=True, db_index=True)
    pev_tram_info_compr = models.IntegerField(null=True, blank=True, db_index=True)
    pev_tram_info_util = models.IntegerField(null=True, blank=True, db_index=True)
    pev_tram_resp_util = models.IntegerField(null=True, blank=True, db_index=True)
    pev_tram_resp_compl = models.IntegerField(null=True, blank=True, db_index=True)
    pev_tram_resp_clara = models.IntegerField(null=True, blank=True, db_index=True)
    pev_tram_acogido = models.IntegerField(null=True, blank=True, db_index=True)

    datos = models.JSONField(default=dict)
