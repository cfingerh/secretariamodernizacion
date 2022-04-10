from sys import excepthook
import ipdb
from load import *
import matplotlib.pyplot as plt

import os
from weasyprint import HTML
from django.template.loader import render_to_string

from base.models import Institucion, Raw, Respuesta

Respuesta.objects.all().delete()
Institucion.objects.filter(nombre_corto='seriviu_araucania').update(nombre_corto='serviu_araucania')
Institucion.objects.filter(nombre_corto='inapu').update(nombre_corto='inapi')

# for anio in [2015,2016,2017,2018]:


class Procesar:
    def __init__(self, nombre_corto, anio, especial=None):
        self.especial = especial
        self.anio = anio
        self.nombre_corto = nombre_corto
        self.institucion = Institucion.objects.get(nombre_corto=nombre_corto)
        raws = Raw.objects.filter(institucion=self.institucion, anio=anio)

        # CHILECOMPRA
        if self.nombre_corto == 'chilecompra' and especial:
            raws = raws.filter(especial=especial)

        self.datos = [d.datos for d in raws]

        if especial:
            for dato in self.datos:
                dato["ESPECIAL"] = especial

        # TERMINA CHILECOMPRA

        self.cantidad = len(self.datos)

        if self.cantidad == 0:
            Respuesta.objects.filter(institucion=self.institucion, anio=anio).delete()
            self.log("No hay datos para para el año ")
            return

        # IPS
        if self.nombre_corto == 'ips' and self.anio == 2019:
            for dato in self.datos:
                if dato.get("PONDERADOR") and dato.get("POND") is None:
                    dato["POND"] = dato.get("PONDERADOR")

        columnas = []
        for dato in self.datos:
            for columna in dato.keys():
                if columna not in columnas:
                    columnas.append(columna)

        self.columnas_originales = []
        for key in self.datos[0].keys():
            if key not in self.columnas_originales:
                self.columnas_originales.append(key)

        for columna in self.columnas_originales:
            for dato in self.datos:
                dato[columna.upper()] = dato.get(columna)

        # if self.nombre_corto in ["chilecompra"] and self.anio == 2015:
        #     for dato in self.datos:
        #         dato["SERVICIO"] = dato.get("SERVICIO") or dato.get("CUOTA_ID")

        # economia y otros el anio 2019
        self.copiar_columna('P11A', 'PH01')
        self.copiar_columna('P11B', 'PH02')
        self.copiar_columna('P11C', 'PH03')
        self.copiar_columna('P11D', 'PH04')

        self.columnas = []
        for key in self.datos[0].keys():
            if key not in self.columnas:
                self.columnas.append(key)

        if not self.limpiar_ponderador():
            return

        self.limpiar_eval_inst()
        self.limpiar_experiencia()
        self.limpiar_habilitacion()

        self.limpiar_imagen_confianza()
        self.limpiar_imagen_transparente()
        self.limpiar_imagen_necesidades()
        self.limpiar_imagen_modernizacion()
        self.limpiar_imagen_comprometidos()
        self.limpiar_imagen_satisface()

        self.limpiar_atributo_facilidad_tramite()
        self.limpiar_atributo_tiempo_respuesta()
        self.limpiar_atributo_claridad_pasos()
        self.limpiar_atributo_comprension_tramite()
        self.limpiar_atributo_informacion_tramite()
        self.limpiar_atributo_utilidad_informacion()
        self.limpiar_atributo_informacion_completa()
        self.limpiar_atributo_calidad_informacion()
        self.limpiar_atributo_acoger_realidad()

        self.limpiar_edades()
        self.contar_edades()

        self.limpiar_tuvo_problema()

        self.limpiar_por_canal()

        self.limpiar_tramite()

        self.limpiar_sexo()
        self.canal_utilizado()
        self.limpiar_region()
        self.limpiar_educacion()

        self.exportar_pdf()
        self.exportar_respuestas()
        self.datos = None

    def log(self, texto):
        print(self.nombre_corto, self.anio, texto)

    def copiar_columna(self, origen, destino):
        for dato in self.datos:
            if origen in dato.keys():
                dato[destino] = dato.get(origen)

    def limpiar_valores_de_columna(self, columna):
        for dato in self.datos:
            dato[columna] = self.limpiar_valor(dato.get(columna))

    def limpiar_valor_experiencia(self, valor):
        try:
            valor = int(valor.split(" ")[0])
        except:
            pass

        try:
            if valor.lower().find("no leer") >= 0:
                return None
        except:
            pass

        try:
            if valor.lower().find("null") >= 0:
                return None
        except:
            pass

        return valor

    def limpiar_valor_educacion(self, valor):
        valor = self.limpiar_valor(valor)
        try:
            return int(valor.split(".")[0])
        except:
            pass
        return valor

    def limpiar_valor_region(self, valor):
        valor = self.limpiar_valor(valor)
        try:
            if valor.lower().find('null') >= 0:
                return None
        except:
            pass

        if valor is None:
            return None

        try:
            int(valor)
            return valor
        except:
            pass

        if valor.lower().find('&') >= 0 or valor.lower() == '-':
            return None
        if valor.lower().find('1970') >= 0 or valor.lower() == '-':
            return None
        if valor.lower().find('no aplica') >= 0 or valor.lower().find('no identi') >= 0 or valor.lower().find('oficina centr') >= 0 or valor.lower().find("sin valor") >= 0:
            return None

        if valor.lower().find("tarapac") >= 0 or valor.lower().find("i reg") == 0 or valor.lower().find("iquique") == 0:
            return 1
        if valor.lower().find("antofagast") >= 0 or valor.lower().find("ii reg") == 0 or valor.lower().find("calama") >= 0:
            return 2
        if valor.lower().find("atacama") >= 0 or valor.lower().find("iii reg") == 0:
            return 3
        if valor.lower().find("coquimbo") >= 0 or valor.lower().find("iv reg") == 0 or valor.lower().find("ovalle") >= 0:
            return 4
        if valor.lower().find("valpara") >= 0 or valor.lower().find("v reg") == 0:
            return 5
        if valor.lower().find("higgins") >= 0 or valor.lower().find("vi reg") == 0:
            return 6
        if valor.lower().find("maule") >= 0 or valor.lower().find("vii reg") == 0:
            return 7
        if valor.lower().find("biob") >= 0 or valor.lower().find("bio-b") >= 0 or valor.lower().find("bio b") >= 0 or valor.lower().find("bío b") >= 0 or valor.lower().find("viii reg") == 0:
            return 8
        if valor.lower().find("bío-bío") >= 0 or valor.lower().find("bíobío") >= 0:
            return 8
        if valor.lower().find("araucan") >= 0 or valor.lower().find("ix reg") == 0:
            return 9
        if valor.lower().find("los lagos") >= 0 or valor.lower().find("x reg") == 0 or valor.lower().find("montt") >= 0 or valor.lower().find("chiloé") >= 0 or valor.lower().find("osorno") >= 0 or valor.lower().find("palena") >= 0:
            return 10
        if valor.lower().find("del campo") >= 0 or valor.lower().find("aysén") >= 0 or valor.lower().find("aisén") >= 0 or valor.lower().find("aysen") >= 0:
            return 11
        if valor.lower().find("magallane") >= 0 or valor.lower().find("xii reg") == 0:
            return 12
        if valor.lower().find("metropolit") >= 0 or valor.lower().find("xiii reg") == 0 or valor.lower().find("rm reg") == 0:
            return 13
        if valor.lower().find("los rios") >= 0 or valor.lower().find("los ríos") >= 0 or valor.lower().find("xiv reg") == 0 or valor.lower().find("la uni") >= 0:
            return 14
        if valor.lower().find("arica") >= 0 or valor.lower().find("xv reg") == 0:
            return 15
        if valor.lower().find("ñuble") >= 0 or valor.lower().find("nuble") >= 0 or valor.lower().find("xvi reg") == 0:
            return 9

        return valor

    def limpiar_valor(self, valor):
        """pasa a integer y 8 a 88 y 9 a 99"""

        try:
            if valor.find("NO LEER") >= 0:
                return None
        except:
            pass

        try:
            if valor.strip() == '-':
                return None
        except:
            pass

        try:
            valor = float(valor)
        except:
            pass

        try:
            valor = int(valor)
        except:
            pass

        if valor == 8:
            valor = 88

        if valor == 9 or valor == 999:
            valor = 99

        return valor

    def obtener_absolutos(self, negativo, positivo, respondido, universo):
        if float(respondido) == 0:
            return {"solo_respondidos": {}, "incluye_todos": {}}

        solo_respondidos = {
            "positivo": round(float(positivo) / float(respondido), 3),
            "negativo": round(float(negativo) / float(respondido), 3),
        }
        solo_respondidos["diferencia"] = solo_respondidos["positivo"] - solo_respondidos["negativo"]
        solo_respondidos["absoluto"] = round(solo_respondidos["positivo"], 2) - round(solo_respondidos["negativo"], 2)

        incluye_todos = {
            "positivo": round(float(positivo) / float(universo), 3),
            "negativo": round(float(negativo) / float(universo), 3),
        }
        incluye_todos["diferencia"] = incluye_todos["positivo"] - incluye_todos["negativo"]
        incluye_todos["absoluto"] = round(incluye_todos["positivo"], 2) - round(incluye_todos["negativo"], 2)

        return {"solo_respondidos": solo_respondidos, "incluye_todos": incluye_todos}

    def limpiar_habilitacion(self):
        columnas_posibles = ["H1_X", "PH0X", "PH01_X", "P11_XR", "P11_X"]

        columna = None
        for columna_posible in columnas_posibles:
            if (columna_posible.replace("X", "4") in self.columnas or columna_posible.replace("X", "3") in self.columnas) and columna is None:
                for dato in self.datos:
                    if (dato.get(columna_posible.replace("X", "4")) or dato.get(columna_posible.replace("X", "3"))) and columna is None:
                        columna = columna_posible

        if not columna:
            self.log("No se encontró columna para habilitacion")
            return

        habilitacion_1 = columna.replace("X", "1")
        habilitacion_2 = columna.replace("X", "2")
        habilitacion_3 = columna.replace("X", "3")
        habilitacion_4 = columna.replace("X", "4")

        self.habilitacion_1 = {"columna": habilitacion_1 if habilitacion_1 in self.columnas else None}
        self.habilitacion_2 = {"columna": habilitacion_2 if habilitacion_2 in self.columnas else None}
        self.habilitacion_3 = {"columna": habilitacion_3 if habilitacion_3 in self.columnas else None}
        self.habilitacion_4 = {"columna": habilitacion_4 if habilitacion_4 in self.columnas else None}

        self.limpiar_valores_de_columna(habilitacion_1)
        self.limpiar_valores_de_columna(habilitacion_2)
        self.limpiar_valores_de_columna(habilitacion_3)
        self.limpiar_valores_de_columna(habilitacion_4)

        self.habilitacion_1["registros"] = self.get_registro_de_valores(habilitacion_1)
        self.habilitacion_2["registros"] = self.get_registro_de_valores(habilitacion_2)
        self.habilitacion_3["registros"] = self.get_registro_de_valores(habilitacion_3)
        self.habilitacion_4["registros"] = self.get_registro_de_valores(habilitacion_4)

        for dato in self.datos:
            valor_1 = self.limpiar_valor(dato.get(self.habilitacion_1["columna"]))
            valor_2 = self.limpiar_valor(dato.get(self.habilitacion_2["columna"]))
            valor_3 = self.limpiar_valor(dato.get(self.habilitacion_3["columna"]))
            valor_4 = self.limpiar_valor(dato.get(self.habilitacion_4["columna"]))

            hbs = [h for h in [valor_1, valor_2, valor_3, valor_4] if h and h <= 7]
            if len(hbs) > 0:
                dato["habilitacion_promedio"] = sum(hbs) / len(hbs)
            else:
                dato["habilitacion_promedio"] = None

            if dato["habilitacion_promedio"] and dato["habilitacion_promedio"] < 4.5:
                dato["habilitacion_grupo_cf"] = 1
            if dato["habilitacion_promedio"] and dato["habilitacion_promedio"] >= 4.5 and dato["habilitacion_promedio"] < 5.5:
                dato["habilitacion_grupo_cf"] = 2
            if dato["habilitacion_promedio"] and dato["habilitacion_promedio"] >= 5.5 and dato["habilitacion_promedio"] <= 7:
                dato["habilitacion_grupo_cf"] = 3

        # Evaluacion Institucion
        # No habilitados
        seleccion = [dato for dato in self.datos if dato["habilitacion_promedio"] and dato["habilitacion_promedio"] < 4.5]
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["eval_inst"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["eval_inst"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["eval_inst"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])

        self.eval_inst_no_habilitados = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("eval_inst")}

        # Meidanamente habilitados
        seleccion = [dato for dato in self.datos if dato["habilitacion_promedio"] and dato["habilitacion_promedio"] >= 4.5 and dato["habilitacion_promedio"] < 5.5]
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["eval_inst"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["eval_inst"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["eval_inst"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])

        self.eval_inst_medianamente_habilitados = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("eval_inst")}

        # habilitados
        seleccion = [dato for dato in self.datos if dato["habilitacion_promedio"] and dato["habilitacion_promedio"] >= 5.5 and dato["habilitacion_promedio"] <= 7]
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["eval_inst"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["eval_inst"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["eval_inst"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])

        self.eval_inst_habilitados = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("eval_inst")}

        # ULTIMA EXPERIENCIA
        # No habilitados
        seleccion = [dato for dato in self.datos if dato["habilitacion_promedio"] and dato["habilitacion_promedio"] < 4.5]
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])

        self.experiencia_no_habilitados = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("experiencia")}

        # Meidanamente habilitados
        seleccion = [dato for dato in self.datos if dato["habilitacion_promedio"] and dato["habilitacion_promedio"] >= 4.5 and dato["habilitacion_promedio"] < 5.5]
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])

        self.experiencia_medianamente_habilitados = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("experiencia")}

        # habilitados
        seleccion = [dato for dato in self.datos if dato["habilitacion_promedio"] and dato["habilitacion_promedio"] >= 5.5 and dato["habilitacion_promedio"] <= 7]
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])

        self.experiencia_habilitados = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("experiencia")}

    def get_registro_de_valores(self, columna):
        registros = {}

        for dato in self.datos:
            valor = dato.get(columna)

            if valor is None:
                continue
            registros[valor] = registros.get(valor, 0) + 1

        valores = list(set(registros.keys()))
        try:
            valores.sort()
        except:
            pass

        _registros = {}
        for valor in valores:
            _registros[valor] = registros[valor]
        return _registros

    def limpiar_eval_inst(self):
        if self.anio <= 2019:
            columnas_posibles = ["P1", "P1_1"]
        elif self.anio == 2020:
            columnas_posibles = ["PI2"]
        elif self.anio == 2021:
            columnas_posibles = ["PI2", "PI02"]

        columna = None
        for columna_posible in columnas_posibles:
            if columna_posible in self.columnas:
                columna = columna_posible

        if not columna:
            self.log("No se encontró columna para eval_inst")
            return

        self.columna_eval_inst = columna

        valores = []

        for dato in self.datos:
            valor = dato[columna]
            valor = self.limpiar_valor(valor)
            valor = self.limpiar_valor_experiencia(valor)
            dato["eval_inst"] = valor
            valores.append(valor)

        valores = list(set(valores))
        negativo = sum([float(d["PONDERADOR"]) for d in self.datos if d["eval_inst"] in [1, 2, 3, 4]])
        positivo = sum([float(d["PONDERADOR"]) for d in self.datos if d["eval_inst"] in [6, 7]])
        respondido = sum([float(d["PONDERADOR"]) for d in self.datos if d["eval_inst"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([float(d["PONDERADOR"]) for d in self.datos])

        self.eval_inst = {"absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
                          "registros": self.get_registro_de_valores("eval_inst")}

    def limpiar_experiencia(self):
        if self.anio <= 2019:
            columnas_posibles = ["P2", "P2_1"]
        elif self.anio == 2020:
            columnas_posibles = ["PEX05"]
        elif self.anio == 2021:
            columnas_posibles = ["PEX05"]

        columna = None
        for columna_posible in columnas_posibles:
            if columna_posible in self.columnas:
                columna = columna_posible

        if not columna:
            self.log("No se encontró columna para experiencia")
            return

        self.columna_experiencia = columna

        valores = []

        for dato in self.datos:
            valor = dato[columna]
            valor = self.limpiar_valor(valor)
            valor = self.limpiar_valor_experiencia(valor)
            int(valor or 0)
            dato["experiencia"] = valor
            valores.append(valor)

        valores = list(set(valores))
        negativo = sum([d["PONDERADOR"] for d in self.datos if d["experiencia"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in self.datos if d["experiencia"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in self.datos if d["experiencia"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in self.datos])

        self.experiencia = {"absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
                            "registros": self.get_registro_de_valores("eval_inst")}

    def limpiar_ponderador(self):
        columnas_posibles = ["PONDERADOR", "POND1", "F_POND", "PONDERADOR2", "POND"]

        columna = None
        for columna_posible in columnas_posibles:
            if columna_posible in self.columnas:
                columna = columna_posible

        if not columna:
            self.log("No se encontró columna para ponderador")
            return

        self.columna_ponderador = columna

        valores = []

        for dato in self.datos:
            dato["PONDERADOR"] = float(dato[columna]) if dato[columna] else 0
            if dato["PONDERADOR"] > 0:
                valores.append(dato["PONDERADOR"])

        self.ponderador_avg = round(sum(valores) / len(valores), 4)
        valores = list(set(valores))
        self.ponderador_columna = columna
        self.ponderador_max = max(valores)
        self.ponderador_min = min(valores)
        self.ponderador_rel = max(valores) / min(valores)

        return True

    def find_columna(self, nombre, columnas_posibles):
        columna = None

        for columna_posible in columnas_posibles:
            if columna_posible in self.columnas:
                columna = columna_posible
                break

        if not columna:
            self.log("No se encontró columna para {}".format(nombre))
            return False

        setattr(self, nombre, columna)
        return True

    def limpiar_region(self):
        columnas_posibles = ["REGION", "REGIONES", "BANNER_REGION"]

        if not self.find_columna("columna_region", columnas_posibles):
            return

        for dato in self.datos:
            valor = dato.get(self.columna_region)
            valor = self.limpiar_valor_region(valor)

            dato["region_cf"] = valor

        self.registro_regiones = self.get_registro_de_valores("region_cf")

    def limpiar_educacion(self):
        if self.anio == 2015:
            columnas_posibles = ["P19_2"]
            if self.find_columna("columna_educacion", columnas_posibles):
                for dato in self.datos:
                    valor = dato.get(self.columna_educacion)
                    if self.limpiar_valor(valor) in [1, 2]:
                        grupo = 'Enseñanza Básica'
                    elif self.limpiar_valor(valor) in [3, 4, 5]:
                        grupo = 'Enseñanza Media'
                    elif self.limpiar_valor(valor) in [6, 7]:
                        grupo = 'Superior'
                    else:
                        grupo = self.limpiar_valor(valor)
                    dato["educacion_agrupada_cf"] = grupo
            return

        elif self.anio == 2016:
            columnas_posibles = ["P22"]
        elif self.anio == 2017:
            columnas_posibles = ["P19"]
            if self.nombre_corto in ['chilecompra', 'sernac', 'ine']:
                # OJO Chilecompra también tiene P22, pero con otra codificacion
                columnas_posibles = ["P20"]
        elif self.anio == 2018:
            columnas_posibles = ["P24"]
            if self.nombre_corto in ["registrocivil"]:
                columnas_posibles = ["P27"]  # ojo que el de instituciones de registro civil apra el 2018 tiene otras columnas. No se está importando por ahora
        elif self.anio == 2019:
            columnas_posibles = ["edujefe", "P24"]
        elif self.anio == 2020:
            columnas_posibles = ["UN7"]
        elif self.anio == 2021:
            columnas_posibles = ["EDUC_AGR", "N7"]

        if not self.find_columna("columna_educacion", columnas_posibles):
            return

        for dato in self.datos:
            if self.anio in [2015]:
                valor = dato.get(self.columna_educacion)
                if self.limpiar_valor(valor) in [1, 2, 3, 4]:
                    grupo = 'Enseñanza Básica'
                elif self.limpiar_valor(valor) in [5, 6, 8]:
                    grupo = 'Enseñanza Media'
                elif self.limpiar_valor(valor) in [7, 9, 10, 11]:
                    grupo = 'Superior'
                elif self.limpiar_valor(valor) in [12]:
                    grupo = '99'
                else:
                    grupo = self.limpiar_valor(valor)

            elif self.anio in [2016]:
                valor = dato.get(self.columna_educacion)
                if self.limpiar_valor(valor) in [1, 2, 3, 4]:
                    grupo = 'Enseñanza Básica'
                elif self.limpiar_valor(valor) in [5, 6, 8]:
                    grupo = 'Enseñanza Media'
                elif self.limpiar_valor(valor) in [7, 9, 10]:
                    grupo = 'Superior'
                elif self.limpiar_valor(valor) in [12]:
                    grupo = '99'
                else:
                    grupo = self.limpiar_valor(valor)

            elif self.anio in [2017]:
                valor = dato.get(self.columna_educacion)

                valor = dato.get(self.columna_educacion)
                if self.limpiar_valor(valor) in [1, 2, 3, 4]:
                    grupo = 'Enseñanza Básica'
                elif self.limpiar_valor(valor) in [5, 6, 8]:
                    grupo = 'Enseñanza Media'
                elif self.limpiar_valor(valor) in [7, 9, 10, 11]:
                    grupo = 'Superior'
                elif self.limpiar_valor(valor) in [12]:
                    grupo = '99'
                else:
                    grupo = self.limpiar_valor(valor)

                # elif self.nombre_corto in ['chilecompra'] and self.especial == 'Proveedor':
                #     valor = dato.get(self.columna_educacion)
                #     if self.limpiar_valor(valor) in [1, 2, 3, 4]:
                #         grupo = 'Enseñanza Básica'
                #     elif self.limpiar_valor(valor) in [5, 6, 8]:
                #         grupo = 'Enseñanza Media'
                #     elif self.limpiar_valor(valor) in [7, 9, 10, 11]:
                #         grupo = 'Superior'
                #     elif self.limpiar_valor(valor) in [12]:
                #         grupo = '99'
                #     else:
                #         grupo = self.limpiar_valor(valor)

                # else:
                #     valor = dato.get(self.columna_educacion)
                #     if self.limpiar_valor(valor) in [1, 2, 3]:
                #         grupo = 'Enseñanza Básica'
                #     elif self.limpiar_valor(valor) in [4, 5]:
                #         grupo = 'Enseñanza Media'
                #     elif self.limpiar_valor(valor) in [6, 7]:
                #         grupo = 'Superior'
                #     elif self.limpiar_valor(valor) in [12]:
                #         grupo = '99'
                #     else:
                #         grupo = self.limpiar_valor(valor)

            elif self.anio in [2018]:
                valor = dato.get(self.columna_educacion)
                if self.limpiar_valor(valor) in [1, 2, 3, 4]:
                    grupo = 'Enseñanza Básica'
                elif self.limpiar_valor(valor) in [5, 6, 8]:
                    grupo = 'Enseñanza Media'
                elif self.limpiar_valor(valor) in [7, 9, 10, 11]:
                    grupo = 'Superior'
                elif self.limpiar_valor(valor) in [12]:
                    grupo = '99'
                else:
                    grupo = self.limpiar_valor(valor)

            elif self.anio in [2019]:
                valor = dato.get(self.columna_educacion)
                if self.limpiar_valor(valor) in [1, 2, 3, 4]:
                    grupo = 'Enseñanza Básica'
                elif self.limpiar_valor(valor) in [5, 6, 8]:
                    grupo = 'Enseñanza Media'
                elif self.limpiar_valor(valor) in [7, 9, 10, 11]:
                    grupo = 'Superior'
                elif self.limpiar_valor(valor) in [12]:
                    grupo = '99'
                else:
                    grupo = self.limpiar_valor(valor)

            elif self.anio in [2020]:
                valor = dato.get(self.columna_educacion)
                if self.limpiar_valor(valor) in [1, 2, 3, 4]:
                    grupo = 'Enseñanza Básica'
                elif self.limpiar_valor(valor) in [5, 6, 8]:
                    grupo = 'Enseñanza Media'
                elif self.limpiar_valor(valor) in [7, 9, 10, 11]:
                    grupo = 'Superior'
                elif self.limpiar_valor(valor) in [12]:
                    grupo = '99'
                else:
                    grupo = self.limpiar_valor(valor)

            elif self.anio in [2021]:
                if self.nombre_corto in ['dicrep', 'isl', 'suseso', 'superpensiones', 'dipreca', 'bienesnacionales', 'sence', 'capredena', 'sec', 'dt', 'ips']:
                    valor = dato.get(self.columna_educacion)
                    if self.limpiar_valor_educacion(valor) in [1, 2, 3, 4]:
                        grupo = 'Enseñanza Básica'
                    elif self.limpiar_valor_educacion(valor) in [5, 6, 8]:
                        grupo = 'Enseñanza Media'
                    elif self.limpiar_valor_educacion(valor) in [7, 9, 10, 11]:
                        grupo = 'Superior'
                    elif self.limpiar_valor_educacion(valor) in [12, 98, 99]:
                        grupo = '99'
                    else:
                        grupo = self.limpiar_valor(valor)
                else:
                    valor = dato.get(self.columna_educacion)
                    if self.limpiar_valor(valor) in [1]:
                        grupo = 'Enseñanza Básica'
                    elif self.limpiar_valor(valor) in [2]:
                        grupo = 'Enseñanza Media'
                    elif self.limpiar_valor(valor) in [3]:
                        grupo = 'Superior'
                    else:
                        grupo = self.limpiar_valor(valor)

            dato["educacion_agrupada_cf"] = grupo

    def limpiar_tramite(self):
        columnas_posibles = []
        if self.anio in [2015]:
            if self.nombre_corto in ["ine"]:
                columnas_posibles = ["TIPO_USUARIO"]
            if self.nombre_corto in ["sernac"]:
                columnas_posibles = ["SERVICIO"]
            if self.nombre_corto in ["chilecompra"]:
                if self.especial == 'Comprador':
                    columnas_posibles = ["SERVICIO"]
                if self.especial == 'Proveedor':
                    columnas_posibles = ["CUOTA_ID"]

        elif self.anio in [2016]:
            columnas_posibles = ["TIPO", "SEG1"]

        elif self.anio == 2017:
            if self.nombre_corto in ["chilecompra"]:
                columnas_posibles = ["SECTOR_REC", "TAMAÃ\x91O"]
            if self.nombre_corto in ["sernac"]:
                columnas_posibles = ["F3"]
            if self.nombre_corto in ["registrocivil"]:
                columnas_posibles = ["P2A"]
            if self.nombre_corto in ["ine"]:
                columnas_posibles = ["Segmento_Usuarios_INE"]

        elif self.anio == 2018:
            columnas_posibles = ["TRAMITE"]
            if self.nombre_corto in ["tesoreria"]:
                columnas_posibles = ["CANAL"]
            if self.nombre_corto in ["cultura"]:
                columnas_posibles = ["F3"]
            if self.nombre_corto in ["sii"]:
                columnas_posibles = ["SEGEM"]

        elif self.anio == 2019:
            if self.nombre_corto in ["economia", "sernac", "ine", "registrocivil", "tesoreria", "chilecompra"]:
                columnas_posibles = ["SERVICIO"]

            if self.nombre_corto in ["dt", "suseso", "superpensiones", "isl", "fonasa", "saludpublica"]:
                columnas_posibles = ["TRAMITE"]
            if self.nombre_corto in ["fosis"]:
                columnas_posibles = ["F3_COD_1"]
            if self.nombre_corto in ["supersalud"]:
                columnas_posibles = ["TRAMITE"]

        elif self.anio == 2020:
            columnas_posibles = ["BD_IDTRAMITE"]
            if self.nombre_corto in ["dipreca"]:
                columnas_posibles = ["BD_segmento1"]

        elif self.anio == 2021:
            if self.nombre_corto in ["tesoreria", "cmf", "scj", "sii", "aduana", "serviciocivil", "cultura", "chilecompra", "serviu"]:
                columnas_posibles = ["BD_NOMBRE_TRÁMITE"]
            else:
                columnas_posibles = ["BD_IDTRAMITE", "COD_TIPO", "TRAMITE"]

        if not self.find_columna("columna_tramite", columnas_posibles):
            return

    def limpiar_sexo(self):
        if self.anio == 2015:
            columnas_posibles = ["BANNER_GENERO"]

        elif self.anio == 2016:
            columnas_posibles = ["SEXO", "P24"]
        elif self.anio == 2016:
            columnas_posibles = ["SEXO", "P24"]
        elif self.anio == 2017:
            if self.nombre_corto in ["registrocivil", "ips"]:
                columnas_posibles = ["P17"]
            else:
                columnas_posibles = ["P18"]
        elif self.anio == 2018:
            if self.nombre_corto in ["suseso"]:
                columnas_posibles = ["P20"]
            else:
                columnas_posibles = ["SEXO"]
        elif self.anio == 2019:
            if self.nombre_corto in ["sernac", "economia", "tesoreria"]:
                columnas_posibles = ["P20"]
            else:
                columnas_posibles = ["SEXO", "SEXO_CAB"]
        elif self.anio == 2020:
            columnas_posibles = ["U2"]
        elif self.anio == 2021:
            columnas_posibles = ["U2"]
            if self.nombre_corto in ["vivienda"]:
                columnas_posibles = ["UN2"]

        if not self.find_columna("columna_sexo", columnas_posibles):
            return

        for dato in self.datos:
            valor = dato.get(self.columna_sexo)
            if valor in [1, '1', 'Hombre']:
                dato["sexo_cf"] = "Hombre"
            elif valor in [2, '2', 'Mujer']:
                dato["sexo_cf"] = "Mujer"
            else:
                dato["sexo_cf"] = valor

        # Hombres
        seleccion = [d for d in self.datos if d.get("sexo_cf") == 'Hombre']
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])
        self.hombres = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("eval_inst")}

        # Mujeres
        seleccion = [d for d in self.datos if d.get("sexo_cf") == 'Mujer']
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])
        self.mujeres = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("eval_inst")}

    def canal_utilizado(self):
        columnas_posibles = ["BD_CANAL", "CANAL", "PEX02_REC", "PEX02"]

        if not self.find_columna("columna_canal_utilizado", columnas_posibles):
            return

        for dato in self.datos:
            valor = dato.get(self.columna_canal_utilizado)
            dato["canal_utilizado"] = valor

    def can(self):
        if self.anio == 2015:
            columnas_posibles = ["BANNER_GENERO"]

        elif self.anio == 2016:
            columnas_posibles = ["SEXO", "P24"]
        elif self.anio == 2016:
            columnas_posibles = ["SEXO", "P24"]
        elif self.anio == 2017:
            if self.nombre_corto in ["registrocivil", "ips"]:
                columnas_posibles = ["P17"]
            else:
                columnas_posibles = ["P18"]
        elif self.anio == 2018:
            if self.nombre_corto in ["suseso"]:
                columnas_posibles = ["P20"]
            else:
                columnas_posibles = ["SEXO"]
        elif self.anio == 2019:
            if self.nombre_corto in ["sernac", "economia", "tesoreria"]:
                columnas_posibles = ["P20"]
            else:
                columnas_posibles = ["SEXO", "SEXO_CAB"]
        elif self.anio == 2020:
            columnas_posibles = ["U2"]
        elif self.anio == 2021:
            columnas_posibles = ["U2"]
            if self.nombre_corto in ["vivienda"]:
                columnas_posibles = ["UN2"]

        if not self.find_columna("columna_sexo", columnas_posibles):
            return

        for dato in self.datos:
            valor = dato.get(self.columna_sexo)
            if valor in [1, '1', 'Hombre']:
                dato["sexo_cf"] = "Hombre"
            elif valor in [2, '2', 'Mujer']:
                dato["sexo_cf"] = "Mujer"
            else:
                dato["sexo_cf"] = valor

        # Hombres
        seleccion = [d for d in self.datos if d.get("sexo_cf") == 'Hombre']
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])
        self.hombres = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("eval_inst")}

        # Mujeres
        seleccion = [d for d in self.datos if d.get("sexo_cf") == 'Mujer']
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])
        self.mujeres = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("eval_inst")}

    def limpiar_por_canal(self):
        if self.anio == 2015:
            if self.nombre_corto in ['ine']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P7_1"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P7_3"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P7_4"))

            elif self.nombre_corto in ['sernac']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P7_1"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P7_2"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P7_3"))

            elif self.nombre_corto == 'chilecompra':
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P7_1"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P7_2")) or self.limpiar_valor(dato.get("P7_3"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P7_4"))
            elif self.nombre_corto in ['ips']:
                a = 1

        if self.anio == 2016:
            if self.nombre_corto in ['sii']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P12_1"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P12_2"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P12_3"))
            elif self.nombre_corto in ['suseso', 'dt']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P8_1"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P8_2"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P8_3"))

        if self.anio == 2017:
            if self.nombre_corto in ['ine', 'registrocivil', 'sernac']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P12_1"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P12_2"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P12_3"))
            elif self.nombre_corto in ['chilecompra']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P7_1"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P7_2")) or self.limpiar_valor(dato.get("P7_3"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P7_4"))
            elif self.nombre_corto in ['ips']:
                a = 1

        if self.anio == 2018:
            if self.nombre_corto in ['cultura', 'ips', 'fonasa', 'registrocivil', 'suseso', 'tesoreria']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P8_1"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P8_2"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P8_3"))
            elif self.nombre_corto in ['dt']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P6_1"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P6_2"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P6_3"))
            elif self.nombre_corto in ['sii']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P12_1"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P12_2"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P12_3"))
            elif self.nombre_corto in ['saludpublica']:
                a = 1

        if self.anio == 2019:
            if self.nombre_corto in ['dt', 'fonasa', 'isl', 'supersalud', 'suseso', 'superpensiones']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P8a"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P8b"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P8c"))
            elif self.nombre_corto in ['chilecompra']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P8a"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P8c"))  # se considera solo la neuva página milicenciamedica.cl y nop la antigua infocompin.cl
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P8d"))
            elif self.nombre_corto in ['vivienda']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P8a_1"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P8b_1"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P8c_1"))
            elif self.nombre_corto in ['fosis', 'registro_civil', 'tesoreria', 'ine', 'sernac', 'economia']:
                for dato in self.datos:
                    dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("P8_1"))
                for dato in self.datos:
                    dato["pec_eval_web"] = self.limpiar_valor(dato.get("P8_2"))
                for dato in self.datos:
                    dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("P8_3"))
            elif self.nombre_corto in ['saludpublica', 'ips']:
                a = 1

        if self.anio == 2020:
            # if self.nombre_corto in ['aduana', 'chilecompra', 'dicrep', 'dt', 'tesoreria', 'vivienda', 'suseso']:
            for dato in self.datos:
                dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("PEC04_1"))
                dato["pec_eval_web"] = self.limpiar_valor(dato.get("PEC04_2"))
                dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("PEC04_3"))

            for dato in self.datos:
                dato["pec_canal_telefono"] = self.limpiar_valor(dato.get("PEC01_01")) or self.limpiar_valor(
                    dato.get("PEC01_100")) or self.limpiar_valor(dato.get("PEC03_100")) or self.limpiar_valor(dato.get("PEC01_1"))
                dato["pec_canal_web"] = self.limpiar_valor(dato.get("PEC01_02")) or self.limpiar_valor(
                    dato.get("PEC01_200")) or self.limpiar_valor(dato.get("PEC03_200")) or self.limpiar_valor(dato.get("PEC01_2"))
                dato["pec_canal_oficina"] = self.limpiar_valor(dato.get("PEC01_03")) or self.limpiar_valor(
                    dato.get("PEC01_300")) or self.limpiar_valor(dato.get("PEC03_300")) or self.limpiar_valor(dato.get("PEC01_3"))
            # else:
            #     import ipdb
            #     ipdb.set_trace()

        if self.anio == 2021:
            for dato in self.datos:
                dato["pec_eval_telefono"] = self.limpiar_valor(dato.get("PEC04_01"))
            for dato in self.datos:
                dato["pec_eval_web"] = self.limpiar_valor(dato.get("PEC04_02"))
            for dato in self.datos:
                dato["pec_eval_oficina"] = self.limpiar_valor(dato.get("PEC04_03"))

        # for dato in self.datos:
        #     print(dato.get())
    def limpiar_tuvo_problema(self):
        if self.anio == 2015:
            # 1 Si
            # 2 No
            columnas_posibles = ["P11"]

        elif self.anio == 2016:
            # 1 Si
            # 2 No
            columnas_posibles = ["P13"]

        elif self.anio == 2017:
            # 1 Si
            # 2 No
            columnas_posibles = ["P13"]
            if self.nombre_corto in ['chilecompra', 'ips']:
                columnas_posibles = [""]
            if self.nombre_corto in ['ine', 'registrocivil']:
                columnas_posibles = ["P12"]

        elif self.anio == 2018:
            # 1 Si
            # 2 No
            columnas_posibles = ["P13"]

        elif self.anio == 2019:
            # 1 Si
            # 2 No
            columnas_posibles = ["P13"]

        elif self.anio == 2020:
            # 1 Si
            # 2 No
            columnas_posibles = ["PEP01"]

        elif self.anio == 2021:
            columnas_posibles = ["PEP01"]
        else:
            columnas_posibles = []

        self.find_columna("tuvo_problema", columnas_posibles)

        if hasattr(self, "tuvo_problema") is False or self.tuvo_problema is None:
            self.log("no se encontró columna de tuvo_problema")
            return

        for dato in self.datos:
            dato["tuvo_problema"] = self.limpiar_valor(dato.get(self.tuvo_problema))
            if dato["tuvo_problema"] == 'SI':
                dato["tuvo_problema"] = 1
            if dato["tuvo_problema"] == 'NO':
                dato["tuvo_problema"] = 2

    def limpiar_edades(self):
        # 2015 había sólo rango de eddad

        if self.anio == 2015:
            columnas_posibles = ["P16"]
            if self.find_columna("columna_edad", columnas_posibles):
                for dato in self.datos:
                    valor = dato.get(self.columna_edad)
                    if int(valor) in [1, 2]:
                        grupo = '18 a 34 años'
                    elif int(valor) in [3]:
                        grupo = '35 a 44 años'
                    elif int(valor) in [4]:
                        grupo = '45 a 54 años'
                    elif int(valor) in [5, 6, 7]:
                        grupo = '55 años o más'
                    else:
                        grupo = None
                    dato["edad_agrupada_cf"] = grupo
            return

        elif self.anio == 2016:
            columnas_posibles = ["EDAD", "P26"]

        elif self.anio == 2017:
            if self.nombre_corto in ["chilecompra", "ine", "sernac"]:
                columnas_posibles = ["P17"]
            elif self.nombre_corto in ["registrocivil"]:
                columnas_posibles = ["P17"]
            else:
                columnas_posibles = []

            if self.find_columna("columna_edad", columnas_posibles):
                for dato in self.datos:
                    valor = dato.get(self.columna_edad)
                    if int(valor) in [1, 2]:
                        grupo = '18 a 34 años'
                    elif int(valor) in [3]:
                        grupo = '35 a 44 años'
                    elif int(valor) in [4]:
                        grupo = '45 a 54 años'
                    elif int(valor) in [5, 6, 7]:
                        grupo = '55 años o más'
                    else:
                        grupo = None

                    dato["edad_agrupada_cf"] = grupo
            return

        elif self.anio == 2018:
            if self.nombre_corto in ["suseso", "saludpublica", "fonasa", "tesoreria"]:
                columnas_posibles = ["P21"]
            elif self.nombre_corto in ["dt", "cultura"]:
                columnas_posibles = ["P22"]
            elif self.nombre_corto in ["registrocivil"]:
                columnas_posibles = ["P24"]
            elif self.nombre_corto in ["sii"]:
                columnas_posibles = ["P22"]
            else:
                columnas_posibles = []

        elif self.anio == 2019:
            columnas_posibles = ["D2_EDAD", "edad"]

            if self.nombre_corto in ["chilecompra"]:
                columnas_posibles = ["D2_EDAD"]

        elif self.anio == 2020:
            columnas_posibles = ["U3"]
        elif self.anio == 2021:
            columnas_posibles = ["U3"]
            if self.nombre_corto in ["vivienda"]:
                columnas_posibles = ["UN2"]
        else:
            columnas_posibles = []

        self.find_columna("columna_edad", columnas_posibles)

        if hasattr(self, "columna_edad") is False or self.columna_edad is None:
            self.log("no se encontró columna de edad")
            return

        for dato in self.datos:
            valor = int(dato.get(self.columna_edad) or 0)
            if valor > 18 and valor <= 34:
                grupo = '18 a 34 años'
            elif valor > 34 and valor <= 44:
                grupo = '35 a 44 años'
            elif valor > 44 and valor <= 54:
                grupo = '45 a 54 años'
            elif valor > 54:
                grupo = '55 años o más'
            else:
                grupo = None

            dato["edad_agrupada_cf"] = grupo

    def contar_edades(self):
        # self.edades = {
        #     "cantidad_18_a_34": len([d for d in self.datos if d.get("edad_agrupada_cf") == '18 a 34 años']),
        #     "cantidad_35_a_44": len([d for d in self.datos if d.get("edad_agrupada_cf") == '35 a 44 años']),
        #     "cantidad_45_a_54": len([d for d in self.datos if d.get("edad_agrupada_cf") == '45 a 54 años']),
        #     "cantidad_55_o_mas": len([d for d in self.datos if d.get("edad_agrupada_cf") == '55 años o más']),
        # }

        # 18 a 34 años
        seleccion = [d for d in self.datos if d.get("edad_agrupada_cf") == '18 a 34 años']
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])
        self.edad_18_a_34 = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("eval_inst")}

        # 35 a 44 años
        seleccion = [d for d in self.datos if d.get("edad_agrupada_cf") == '35 a 44 años']
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])
        self.edad_35_a_44 = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("eval_inst")}

        # 45 a 54 años
        seleccion = [d for d in self.datos if d.get("edad_agrupada_cf") == '45 a 54 años']
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])
        self.edad_45_a_54 = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("eval_inst")}

        # 55 años o mas
        seleccion = [d for d in self.datos if d.get("edad_agrupada_cf") == '55 años o más']
        negativo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4]])
        positivo = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [6, 7]])
        respondido = sum([d["PONDERADOR"] for d in seleccion if d["experiencia"] in [1, 2, 3, 4, 5, 6, 7]])
        universo = sum([d["PONDERADOR"] for d in seleccion])
        self.edad_55_o_mas = {
            "cantidad": len(seleccion),
            "absolutos": self.obtener_absolutos(negativo, positivo, respondido, universo),
            "registros": self.get_registro_de_valores("eval_inst")}

    def limpiar_imagen_confianza(self):
        if self.anio == 2015:
            columnas_posibles = ["P10_1"]
        if self.anio == 2016:
            columnas_posibles = ["P12_1", "P16_1"]
        if self.anio == 2017:
            columnas_posibles = ["P10_1"]
        if self.anio == 2018:
            columnas_posibles = ["P12_1"]
        if self.anio == 2019:
            columnas_posibles = ["P12_1"]
        if self.anio == 2020:
            columnas_posibles = ["PI3_1"]
        if self.anio == 2021:
            columnas_posibles = ["PI03_1", "PI3_1"]

        self.find_columna("columna_confianza", columnas_posibles)

    def limpiar_imagen_transparente(self):
        if self.anio == 2015:
            columnas_posibles = ["P10_2"]
        if self.anio == 2016:
            columnas_posibles = ["P12_2", "P16_2"]
        if self.anio == 2017:
            columnas_posibles = ["P10_2"]
        if self.anio == 2018:
            columnas_posibles = ["P12_2"]
        if self.anio == 2019:
            columnas_posibles = ["P12_2"]
        if self.anio == 2020:
            columnas_posibles = ["PI3_2"]
        if self.anio == 2021:
            columnas_posibles = ["PI03_2", "PI3_2"]

        self.find_columna("columna_transparente", columnas_posibles)

    def limpiar_imagen_necesidades(self):
        if self.anio == 2015:
            columnas_posibles = ["P10_3"]
        if self.anio == 2016:
            columnas_posibles = ["P12_3", "P16_3"]
        if self.anio == 2017:
            columnas_posibles = ["P10_3"]
        if self.anio == 2018:
            columnas_posibles = ["P12_3"]
        if self.anio == 2019:
            columnas_posibles = ["P12_3"]
        if self.anio == 2020:
            columnas_posibles = ["PI3_3"]
        if self.anio == 2021:
            columnas_posibles = ["PI03_3", "PI3_3"]

        self.find_columna("columna_necesidades", columnas_posibles)

    def limpiar_imagen_modernizacion(self):
        if self.anio == 2015:
            columnas_posibles = ["P10_4"]
        if self.anio == 2016:
            columnas_posibles = ["P12_4", "P16_4"]
        if self.anio == 2017:
            columnas_posibles = ["P10_4"]
        if self.anio == 2018:
            columnas_posibles = ["P12_4"]
        if self.anio == 2019:
            columnas_posibles = ["P12_4"]
        if self.anio == 2020:
            columnas_posibles = ["PI3_4"]
        if self.anio == 2021:
            columnas_posibles = ["PI03_4", "PI3_4"]

        self.find_columna("columna_modernizacion", columnas_posibles)

    def limpiar_imagen_comprometidos(self):
        if self.anio == 2015:
            columnas_posibles = ["P10_5"]
        if self.anio == 2016:
            columnas_posibles = ["P12_5", "P16_5"]
        if self.anio == 2017:
            columnas_posibles = ["P10_5"]
        if self.anio == 2018:
            columnas_posibles = ["P12_5"]
        if self.anio == 2019:
            columnas_posibles = ["P12_5"]
        if self.anio == 2020:
            columnas_posibles = ["PI3_5"]
        if self.anio == 2021:
            columnas_posibles = ["PI03_5", "PI3_5"]

        self.find_columna("columna_comprometidos", columnas_posibles)

    def limpiar_imagen_satisface(self):
        if self.anio == 2015:
            columnas_posibles = ["P10_6"]
        if self.anio == 2016:
            columnas_posibles = ["P12_6", "P16_6"]
        if self.anio == 2017:
            columnas_posibles = ["P10_6"]
        if self.anio == 2018:
            columnas_posibles = ["P12_6"]
        if self.anio == 2019:
            columnas_posibles = ["P12_6"]
        if self.anio == 2020:
            columnas_posibles = ["PI3_6"]
        if self.anio == 2021:
            columnas_posibles = ["PI03_6", "PI3_6"]

        self.find_columna("columna_satisface", columnas_posibles)

    # ATRIBUTOS
    def limpiar_atributo_facilidad_tramite(self):
        if self.anio == 2015:
            columnas_posibles = ["P8_1"]
        if self.anio == 2016:
            columnas_posibles = ["P10_1", "P14_1"]
        if self.anio == 2017:
            columnas_posibles = ["P8_1"]
        if self.anio == 2018:
            columnas_posibles = ["P10_1", "P11_1", "P11_1"]
            if self.nombre_corto == 'sii':
                columnas_posibles = ["P14_1si"]
        if self.anio == 2019:
            columnas_posibles = ["P10_1", "P10A"]
        if self.anio == 2020:
            columnas_posibles = ["PEV02_1", "PEV02A_1"]
        if self.anio == 2021:
            columnas_posibles = ["PEV02_1"]

        self.find_columna("columna_facilidad_tramite", columnas_posibles)

    def limpiar_atributo_tiempo_respuesta(self):
        if self.anio == 2015:
            columnas_posibles = ["P8_2"]
        if self.anio == 2016:
            columnas_posibles = ["P10_2", "P14_2"]
        if self.anio == 2017:
            columnas_posibles = ["P8_2"]
        if self.anio == 2018:
            columnas_posibles = ["P10_2", "P11_2", "P11_2"]
            if self.nombre_corto == 'sii':
                columnas_posibles = ["P14_2"]
        if self.anio == 2019:
            columnas_posibles = ["P10_2", "P10B"]
        if self.anio == 2020:
            columnas_posibles = ["PEV02_2", "PEV02A_2"]
        if self.anio == 2021:
            columnas_posibles = ["PEV02_2"]

        self.find_columna("columna_tiempo_respuesta", columnas_posibles)

    def limpiar_atributo_claridad_pasos(self):
        if self.anio == 2015:
            columnas_posibles = ["P8_3"]
        if self.anio == 2016:
            columnas_posibles = ["P10_3", "P14_3"]
        if self.anio == 2017:
            columnas_posibles = ["P8_3"]
        if self.anio == 2018:
            columnas_posibles = ["P10_3", "P11_3", "P11_3"]
            if self.nombre_corto == 'sii':
                columnas_posibles = ["P14_3"]
        if self.anio == 2019:
            columnas_posibles = ["P10_3", "P10C"]
        if self.anio == 2020:
            columnas_posibles = ["PEV02_3", "PEV02A_3"]
        if self.anio == 2021:
            columnas_posibles = ["PEV02_3"]

        self.find_columna("columna_claridad_pasos", columnas_posibles)

    def limpiar_atributo_comprension_tramite(self):
        columnas_posibles = []

        if self.anio == 2018:
            columnas_posibles = []
        if self.anio == 2019:
            columnas_posibles = []
        if self.anio == 2020:
            columnas_posibles = ["PEV02_4", "PEV02A_4"]
        if self.anio == 2021:
            columnas_posibles = ["PEV02_4"]

        self.find_columna("columna_comprension_tramite", columnas_posibles)

    def limpiar_atributo_informacion_tramite(self):
        if self.anio == 2015:
            columnas_posibles = ["P8_4"]
        if self.anio == 2016:
            columnas_posibles = ["P10_4", "P14_4"]
        if self.anio == 2017:
            columnas_posibles = ["P8_4"]
        if self.anio == 2018:
            columnas_posibles = ["P10_4", "P11_4", "P11_4"]
            if self.nombre_corto == 'sii':
                columnas_posibles = ["P14_4"]
        if self.anio == 2019:
            columnas_posibles = ["P10_4", "P10D"]
        if self.anio == 2020:
            columnas_posibles = ["PEV02_5", "PEV02A_5"]
        if self.anio == 2021:
            columnas_posibles = ["PEV02_5"]

        self.find_columna("columna_informacion_tramite", columnas_posibles)

    def limpiar_atributo_utilidad_informacion(self):
        if self.anio == 2015:
            columnas_posibles = ["P8_5"]
        if self.anio == 2016:
            columnas_posibles = ["P10_5", "P14_5"]
        if self.anio == 2017:
            columnas_posibles = ["P8_5"]
        if self.anio == 2018:
            columnas_posibles = ["P10_5", "P11_5", "P11_5"]
            if self.nombre_corto == 'sii':
                columnas_posibles = ["P14_5"]
        if self.anio == 2019:
            columnas_posibles = ["P10_5", "P10E"]
        if self.anio == 2020:
            columnas_posibles = ["PEV02_6", "PEV02A_6"]
        if self.anio == 2021:
            columnas_posibles = ["PEV02_6"]

        self.find_columna("columna_utilidad_informacion", columnas_posibles)

    def limpiar_atributo_informacion_completa(self):
        if self.anio == 2015:
            columnas_posibles = ["P8_6"]
        if self.anio == 2016:
            columnas_posibles = ["P10_6", "P14_6"]
        if self.anio == 2017:
            columnas_posibles = ["P8_6"]
        if self.anio == 2018:
            columnas_posibles = ["P10_6", "P11_6", "P11_6"]
            if self.nombre_corto == 'sii':
                columnas_posibles = ["P14_6"]
        if self.anio == 2019:
            columnas_posibles = ["P10_6", "P10F"]
        if self.anio == 2020:
            columnas_posibles = ["PEV02_7", "PEV02A_7"]
        if self.anio == 2021:
            columnas_posibles = ["PEV02_7"]

        self.find_columna("columna_informacion_completa", columnas_posibles)

    def limpiar_atributo_calidad_informacion(self):
        if self.anio == 2015:
            columnas_posibles = ["P8_7"]
        if self.anio == 2016:
            columnas_posibles = ["P10_7", "P14_7"]
        if self.anio == 2017:
            columnas_posibles = ["P8_7"]
        if self.anio == 2018:
            columnas_posibles = ["P10_7", "P11_7", "P11_7"]
            if self.nombre_corto == 'sii':
                columnas_posibles = ["P14_7"]
        if self.anio == 2019:
            columnas_posibles = ["P10_7", "P10G"]
        if self.anio == 2020:
            columnas_posibles = ["PEV02_8", "PEV02A_8"]
        if self.anio == 2021:
            columnas_posibles = ["PEV02_8"]

        self.find_columna("columna_calidad_informacion", columnas_posibles)

    def limpiar_atributo_acoger_realidad(self):
        if self.anio == 2015:
            columnas_posibles = ["P8_8"]
        if self.anio == 2016:
            columnas_posibles = ["P10_8", "P14_8"]
        if self.anio == 2017:
            columnas_posibles = ["P8_8"]
        if self.anio == 2018:
            columnas_posibles = ["P10_8", "P11_8", "P11_8"]
            if self.nombre_corto == 'sii':
                columnas_posibles = ["P14_8"]
        if self.anio == 2019:
            columnas_posibles = ["P10_8", "P10H"]
        if self.anio == 2020:
            columnas_posibles = ["PEV02_9", "PEV02A_9"]
        if self.anio == 2021:
            columnas_posibles = ["PEV02_9"]

        self.find_columna("columna_acoger_realidad", columnas_posibles)

    def exportar_pdf(self):
        return
        html_string = render_to_string('base/pdf.html', {'objeto': self, })
        html = HTML(string=html_string,  # base_url=os.getcwd() + "/static/cotizaciones"
                    )
        pdf = html.write_pdf(stylesheets=['base/templates/base/pdf.css'])
        f = open(os.path.join('.', 'resumen', '{}_{}.pdf'.format(self.nombre_corto, self.anio)), 'wb')
        f.write(pdf)

    def exportar_respuestas(self):

        if self.especial not in ['Comprador']:
            Respuesta.objects.filter(institucion=self.institucion, anio=self.anio).delete()

        if self.nombre_corto == 'vivienda' and self.anio == 2020:
            Respuesta.objects.filter(institucion__in=Institucion.objects.filter(nombre_corto__icontains='serviu'), anio=self.anio).delete()

        # if self.nombre_corto == 'vivienda' and self.anio == 2021:
        #     Respuesta.objects.filter(institucion__in=Institucion.objects.filter(nombre_corto__icontains='serviu'), anio=self.anio).delete()

        respuestas = []
        for dato in self.datos:
            respuesta = Respuesta(
                anio=self.anio,
                institucion=self.institucion)

            respuesta.f_pond = dato.get(self.columna_ponderador) if hasattr(self, "columna_ponderador") else None

            respuesta.experiencia = dato.get("experiencia")
            respuesta.eval_inst = dato.get("eval_inst")
            respuesta.edad = dato.get("edad_agrupada_cf")
            respuesta.sexo = dato.get("sexo_cf")
            respuesta.habilitado = dato.get("habilitacion_grupo_cf")
            respuesta.educacion = dato.get("educacion_agrupada_cf")
            respuesta.tuvo_problema = dato.get("tuvo_problema")

            respuesta.pec_eval_telefono = dato.get("pec_eval_telefono")
            respuesta.pec_eval_web = dato.get("pec_eval_web")
            respuesta.pec_eval_presencial = dato.get("pec_eval_oficina")

            respuesta.pec_canal_telefono = dato.get("pec_canal_telefono")
            respuesta.pec_canal_web = dato.get("pec_canal_web")
            respuesta.pec_canal_presencial = dato.get("pec_canal_oficina")

            respuesta.tipo_tramite = self.limpiar_valor_experiencia(dato.get(self.columna_tramite)) if hasattr(self, "columna_tramite") else None
            respuesta.pi_imagen_confianza = self.limpiar_valor_experiencia(dato.get(self.columna_confianza)) if hasattr(self, "columna_confianza") else None
            respuesta.pi_imagen_transp = self.limpiar_valor_experiencia(dato.get(self.columna_transparente)) if hasattr(self, "columna_transparente") else None
            respuesta.pi_imagen_preocupa = self.limpiar_valor_experiencia(dato.get(self.columna_necesidades)) if hasattr(self, "columna_necesidades") else None
            respuesta.pi_imagen_actual = self.limpiar_valor_experiencia(dato.get(self.columna_modernizacion)) if hasattr(self, "columna_modernizacion") else None
            respuesta.pi_imagen_funcion = self.limpiar_valor_experiencia(dato.get(self.columna_comprometidos)) if hasattr(self, "columna_comprometidos") else None
            respuesta.pi_imagen_satisface = self.limpiar_valor_experiencia(dato.get(self.columna_satisface)) if hasattr(self, "columna_satisface") else None

            respuesta.pev_tram_facil = self.limpiar_valor_experiencia(dato.get(self.columna_facilidad_tramite)) if hasattr(self, "columna_facilidad_tramite") else None
            respuesta.pev_tram_tiempo = self.limpiar_valor_experiencia(dato.get(self.columna_tiempo_respuesta)) if hasattr(self, "columna_tiempo_respuesta") else None
            respuesta.pev_tram_claridad_pasos = self.limpiar_valor_experiencia(dato.get(self.columna_claridad_pasos)) if hasattr(self, "columna_claridad_pasos") else None
            respuesta.pev_tram_info_compr = self.limpiar_valor_experiencia(dato.get(self.columna_comprension_tramite)) if hasattr(self, "columna_comprension_tramite") else None
            respuesta.pev_tram_info_util = self.limpiar_valor_experiencia(dato.get(self.columna_informacion_tramite)) if hasattr(self, "columna_informacion_tramite") else None
            respuesta.pev_tram_resp_util = self.limpiar_valor_experiencia(dato.get(self.columna_utilidad_informacion)) if hasattr(self, "columna_utilidad_informacion") else None
            respuesta.pev_tram_resp_compl = self.limpiar_valor_experiencia(dato.get(self.columna_informacion_completa)) if hasattr(self, "columna_informacion_completa") else None
            respuesta.pev_tram_resp_clara = self.limpiar_valor_experiencia(dato.get(self.columna_calidad_informacion)) if hasattr(self, "columna_calidad_informacion") else None
            respuesta.pev_tram_acogido = self.limpiar_valor_experiencia(dato.get(self.columna_acoger_realidad)) if hasattr(self, "columna_acoger_realidad") else None

            datos_originales = {}
            for c in self.columnas_originales:
                datos_originales[c] = dato.get(c)

            datos_originales["region_cf"] = dato.get("region_cf")
            datos_originales["canal_utilizado"] = dato.get("canal_utilizado")
            respuesta.region = dato.get("region_cf")
            respuesta.especial = self.especial

            respuesta.datos = datos_originales

            respuestas.append(respuesta)

        resp = Respuesta.objects.bulk_create(respuestas)


anios = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
# anios = [2021]

# instituciones = Institucion.objects.filter(nombre_corto__isnull=False, pk__in=Raw.objects.filter(anio__in=anios).distinct('institucion').values('institucion')).order_by('-codigo_dipres')
instituciones = Institucion.objects.filter(nombre_corto__isnull=False).order_by('-codigo_dipres')
# instituciones = instituciones.filter(nombre_corto__in=['vivienda'])

import random
for institucion in instituciones:
    print(institucion.nombre_corto)
    completo = []
    # for anio in [2015, 2016, 2017, 2018, 2019, 2020]:
    for anio in anios:
        if anio in [2015, 2017, 2019] and institucion.nombre_corto == 'chilecompra':
            procesar = Procesar(institucion.nombre_corto, anio, especial='Proveedor')
            procesar = Procesar(institucion.nombre_corto, anio, especial='Comprador')
            continue

        procesar = Procesar(institucion.nombre_corto, anio)
        if procesar.cantidad > 0:
            completo.append(procesar)

    institucion.completo = completo


# Generar PDF
html_string = render_to_string('base/completo.html', {'instituciones': instituciones, })
html = HTML(string=html_string,)
pdf = html.write_pdf(stylesheets=['base/templates/base/pdf.css'])
f = open(os.path.join('.', 'resumen', 'completo.pdf'), 'wb')
f.write(pdf)


Respuesta.objects.filter(institucion__nombre_corto='ine', anio=2015, tipo_tramite='1.0').update(tipo_tramite='Público General')
Respuesta.objects.filter(institucion__nombre_corto='ine', anio=2015, tipo_tramite='2.0').update(tipo_tramite='Usuarios Especializados')

Respuesta.objects.filter(institucion__nombre_corto='sernac', anio=2015, tipo_tramite='1.0').update(tipo_tramite='Reclamos en General ')
Respuesta.objects.filter(institucion__nombre_corto='sernac', anio=2015, tipo_tramite='2.0').update(tipo_tramite='Mediaciones Colectivas')


Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Proveedor', anio=2015, tipo_tramite='1.0').update(tipo_tramite='Grande')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Proveedor', anio=2015, tipo_tramite='2.0').update(tipo_tramite='Mediana')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Proveedor', anio=2015, tipo_tramite='3.0').update(tipo_tramite='Pequeña')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Proveedor', anio=2015, tipo_tramite='4.0').update(tipo_tramite='Micro')

Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2015, tipo_tramite='1.0').update(tipo_tramite='FFAA')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2015, tipo_tramite='2.0').update(tipo_tramite='Gobierno Central')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2015, tipo_tramite='3.0').update(tipo_tramite='Legislativo y Judicial')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2015, tipo_tramite='4.0').update(tipo_tramite='Municipalidades')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2015, tipo_tramite='5.0').update(tipo_tramite='Salud')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2015, tipo_tramite='6.0').update(tipo_tramite='Obras Públicas')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2015, tipo_tramite='7.0').update(tipo_tramite='Otros')


Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Proveedor', anio=2017, tipo_tramite='1.0').update(tipo_tramite='Grande')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Proveedor', anio=2017, tipo_tramite='2.0').update(tipo_tramite='Mediana')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Proveedor', anio=2017, tipo_tramite='3.0').update(tipo_tramite='Pequeña')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Proveedor', anio=2017, tipo_tramite='4.0').update(tipo_tramite='Micro')

Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2017, tipo_tramite='1.0').update(tipo_tramite='FFAA')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2017, tipo_tramite='2.0').update(tipo_tramite='Gobierno Central')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2017, tipo_tramite='3.0').update(tipo_tramite='Legislativo y Judicial')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2017, tipo_tramite='4.0').update(tipo_tramite='Municipalidades')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2017, tipo_tramite='5.0').update(tipo_tramite='Salud')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2017, tipo_tramite='6.0').update(tipo_tramite='Obras Públicas')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2017, tipo_tramite='7.0').update(tipo_tramite='Otros')

Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Proveedor', anio=2019, tipo_tramite='1.0').update(tipo_tramite='Atención ciudadana')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Proveedor',
                         anio=2019, tipo_tramite='2.0').update(tipo_tramite='Transacciones en Mercado Público')

Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2019, tipo_tramite='1').update(tipo_tramite='Atención ciudadana')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador', anio=2019, tipo_tramite='2').update(tipo_tramite='Capacitaciones')
Respuesta.objects.filter(institucion__nombre_corto='chilecompra', especial='Comprador',
                         anio=2019, tipo_tramite='3').update(tipo_tramite='Transacciones en Mercado Público')


Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2016, tipo_tramite='1.0').update(tipo_tramite='Licencia Médica')
Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2016, tipo_tramite='2.0').update(tipo_tramite='Seguridad Laboral')
Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2016, tipo_tramite='3.0').update(tipo_tramite='Otras Materias')

Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2016, tipo_tramite='1.0').update(tipo_tramite='Trabajador')
Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2016, tipo_tramite='2.0').update(tipo_tramite='Empleador')
Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2016, tipo_tramite='3.0').update(tipo_tramite='Dirigente (OOSS)')


Respuesta.objects.filter(institucion__nombre_corto='sii', anio=2016, tipo_tramite='1.0').update(tipo_tramite='Persona Natural')
Respuesta.objects.filter(institucion__nombre_corto='sii', anio=2016, tipo_tramite='2.0').update(tipo_tramite='Micro/ Pequeña')
Respuesta.objects.filter(institucion__nombre_corto='sii', anio=2016, tipo_tramite='3.0').update(tipo_tramite='Mediana/ Grande')

Respuesta.objects.filter(institucion__nombre_corto='ine', anio=2017, tipo_tramite='1.0').update(tipo_tramite='Publico General')
Respuesta.objects.filter(institucion__nombre_corto='ine', anio=2017, tipo_tramite='2.0').update(tipo_tramite='Usuarios Especializados Gobierno y Centros de Estudio')
Respuesta.objects.filter(institucion__nombre_corto='ine', anio=2017, tipo_tramite='3.0').update(tipo_tramite='Empresas y Medios')


Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2017, tipo_tramite='1.0').update(
    tipo_tramite='Reservé hora a través de la página web y acudí a oficina a renovar o sacar carnet de identidad')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2017, tipo_tramite='2.0').update(
    tipo_tramite='Reservé horaserviu a través de la página web y acudí a oficina a renovar o sacar pasaporte')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2017, tipo_tramite='3.0').update(tipo_tramite='Solicité Certificado(s)')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2017, tipo_tramite='4.0').update(tipo_tramite='Realicé consulta(s)')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2017, tipo_tramite='5.0').update(tipo_tramite='Solicité información vía Transparencia')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2017, tipo_tramite='6.0').update(tipo_tramite='Puse una Felicitación')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2017, tipo_tramite='7.0').update(tipo_tramite='Coloqué un reclamo')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2017, tipo_tramite='8.0').update(tipo_tramite='Realicé una sugerencia')

Respuesta.objects.filter(institucion__nombre_corto='sernac', anio=2017, tipo_tramite='1.0').update(tipo_tramite='Consulta')
Respuesta.objects.filter(institucion__nombre_corto='sernac', anio=2017, tipo_tramite='2.0').update(tipo_tramite='Reclamo')
Respuesta.objects.filter(institucion__nombre_corto='sernac', anio=2017, tipo_tramite='3.0').update(tipo_tramite='Mediación Colectiva')


Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2018, tipo_tramite='1.0').update(tipo_tramite='Fiscalización')
Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2018, tipo_tramite='2.0').update(tipo_tramite='Mediación')
Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2018, tipo_tramite='3.0').update(tipo_tramite='Conciliación')
Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2018, tipo_tramite='4.0').update(tipo_tramite='Certificados')
Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2018, tipo_tramite='5.0').update(tipo_tramite='Consulta laboral')
Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2018, tipo_tramite='6.0').update(tipo_tramite='Ministro de fe')


Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2018, tipo_tramite='1.0').update(tipo_tramite='Certificado afiliación')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2018, tipo_tramite='2.0').update(tipo_tramite='Compra bono')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2018, tipo_tramite='3.0').update(tipo_tramite='Afiliación')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2018, tipo_tramite='4.0').update(tipo_tramite='Inscripción consultorio')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2018, tipo_tramite='5.0').update(tipo_tramite='Préstamos médicos')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2018, tipo_tramite='6.0').update(tipo_tramite='PAD')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2018, tipo_tramite='7.0').update(tipo_tramite='Solicitud información')

Respuesta.objects.filter(institucion__nombre_corto='sii', anio=2018, tipo_tramite='1.0').update(tipo_tramite='Persona natural')
Respuesta.objects.filter(institucion__nombre_corto='sii', anio=2018, tipo_tramite='2.0').update(tipo_tramite='Micro/pequeña')
Respuesta.objects.filter(institucion__nombre_corto='sii', anio=2018, tipo_tramite='3.0').update(tipo_tramite='Mediana/grande')


Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2018, tipo_tramite='1.0').update(tipo_tramite='Certificados')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2018, tipo_tramite='2.0').update(tipo_tramite='Identificación')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2018, tipo_tramite='3.0').update(tipo_tramite='Registro de vehículos')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2018, tipo_tramite='4.0').update(tipo_tramite='Contacto y transparencia')


Respuesta.objects.filter(institucion__nombre_corto='cultura', anio=2018, tipo_tramite='1.0').update(tipo_tramite='Transferencia de archivos')
Respuesta.objects.filter(institucion__nombre_corto='cultura', anio=2018, tipo_tramite='2.0').update(tipo_tramite='Solicitud presencial')
Respuesta.objects.filter(institucion__nombre_corto='cultura', anio=2018, tipo_tramite='3.0').update(tipo_tramite='Solicitud remota por vía web')
Respuesta.objects.filter(institucion__nombre_corto='cultura', anio=2018, tipo_tramite='4.0').update(tipo_tramite='Solicitud remota por vía correo electrónico')

Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2018, tipo_tramite='1.0').update(tipo_tramite='Fonocomin')
Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2018, tipo_tramite='2.0').update(tipo_tramite='Certificado discapacidad')

Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2018, tipo_tramite='1.0').update(tipo_tramite='Licencia médica')
Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2018, tipo_tramite='2.0').update(tipo_tramite='Seguro Laboral')
Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2018, tipo_tramite='3.0').update(tipo_tramite='Otras materias')

Respuesta.objects.filter(institucion__nombre_corto='tesoreria', anio=2018, tipo_tramite='1.0').update(tipo_tramite='Call Center')
Respuesta.objects.filter(institucion__nombre_corto='tesoreria', anio=2018, tipo_tramite='2.0').update(tipo_tramite='Atención Presencial')
Respuesta.objects.filter(institucion__nombre_corto='tesoreria', anio=2018, tipo_tramite='3.0').update(tipo_tramite='Formulario Web')


Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2019, tipo_tramite='1.0').update(tipo_tramite='Fiscalizaciones')
Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2019, tipo_tramite='2.0').update(tipo_tramite='Conciliación')
Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2019, tipo_tramite='3.0').update(tipo_tramite='Certificados')
Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2019, tipo_tramite='4.0').update(tipo_tramite='Consulta laboral')
Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2019, tipo_tramite='5.0').update(tipo_tramite='Ministro de fe')
Respuesta.objects.filter(institucion__nombre_corto='dt', anio=2019, tipo_tramite='6.0').update(tipo_tramite='Portal Mi DT')

Respuesta.objects.filter(institucion__nombre_corto='fosis', anio=2019, tipo_tramite='0.0').update(tipo_tramite='NINGUNO')
Respuesta.objects.filter(institucion__nombre_corto='fosis', anio=2019, tipo_tramite='1.0').update(tipo_tramite='EMPLEABILIDAD')
Respuesta.objects.filter(institucion__nombre_corto='fosis', anio=2019, tipo_tramite='2.0').update(tipo_tramite='EMPRENDIMIENTO')
Respuesta.objects.filter(institucion__nombre_corto='fosis', anio=2019, tipo_tramite='3.0').update(tipo_tramite='HABILITACION SOCIAL')
Respuesta.objects.filter(institucion__nombre_corto='fosis', anio=2019, tipo_tramite='4.0').update(tipo_tramite='Menciona curso/ capacitacion')
Respuesta.objects.filter(institucion__nombre_corto='fosis', anio=2019, tipo_tramite='5.0').update(tipo_tramite='Menciona Fosis s/e')
Respuesta.objects.filter(institucion__nombre_corto='fosis', anio=2019, tipo_tramite='97.0').update(tipo_tramite='No responde')
Respuesta.objects.filter(institucion__nombre_corto='fosis', anio=2019, tipo_tramite='98.0').update(tipo_tramite='No recuerda')
Respuesta.objects.filter(institucion__nombre_corto='fosis', anio=2019, tipo_tramite='99.0').update(tipo_tramite='OTRO')

Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2019, tipo_tramite='1.0').update(tipo_tramite='Inscripción de AP')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2019, tipo_tramite='2.0').update(tipo_tramite='Afiliación')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2019, tipo_tramite='3.0').update(tipo_tramite='Venta MLE')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2019, tipo_tramite='4.0').update(tipo_tramite='Certificados de Afiliación')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2019, tipo_tramite='5.0').update(tipo_tramite='Otros trámites')

Respuesta.objects.filter(institucion__nombre_corto='isl', anio=2019, tipo_tramite='1.0').update(tipo_tramite='Prestaciones Médicas')
Respuesta.objects.filter(institucion__nombre_corto='isl', anio=2019, tipo_tramite='2.0').update(tipo_tramite='Prestaciones Económicas')
Respuesta.objects.filter(institucion__nombre_corto='isl', anio=2019, tipo_tramite='3.0').update(tipo_tramite='Prevención de Riesgos')
Respuesta.objects.filter(institucion__nombre_corto='isl', anio=2019, tipo_tramite='4.0').update(tipo_tramite='Gestión de Cotizantes')

Respuesta.objects.filter(institucion__nombre_corto='ine', anio=2019, tipo_tramite='1.0').update(tipo_tramite='Solicitudes de información')

Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2019, tipo_tramite='1.0').update(tipo_tramite='Cédula de Identidad')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2019, tipo_tramite='2.0').update(tipo_tramite='Emisión de Certificados')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2019, tipo_tramite='3.0').update(tipo_tramite='Otros trámites')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2019, tipo_tramite='4.0').update(tipo_tramite='Pasaportes')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2019, tipo_tramite='5.0').update(tipo_tramite='Reserva de hora')
Respuesta.objects.filter(institucion__nombre_corto='registrocivil', anio=2019, tipo_tramite='6.0').update(tipo_tramite='Trámites relativos a vehículos')


Respuesta.objects.filter(institucion__nombre_corto='sernac', anio=2019, tipo_tramite='1.0').update(tipo_tramite='Realizar consultas sobre la ley del consumidor')
Respuesta.objects.filter(institucion__nombre_corto='sernac', anio=2019, tipo_tramite='2.0').update(tipo_tramite='Reclamo ante SERNAC')
Respuesta.objects.filter(institucion__nombre_corto='sernac', anio=2019, tipo_tramite='3.0').update(tipo_tramite='No Molestar')


Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2019, tipo_tramite='1.0').update(tipo_tramite='Certificado de Discapacidad')
Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2019, tipo_tramite='2.0').update(tipo_tramite='Licencias')
Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2019, tipo_tramite='3.0').update(tipo_tramite='Reclamo Isapres')
Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2019, tipo_tramite='4.0').update(tipo_tramite='Usuario Isapre')
Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2019, tipo_tramite='5.0').update(tipo_tramite='Otros trámites')

Respuesta.objects.filter(institucion__nombre_corto='superpensiones', anio=2019, tipo_tramite='1.0').update(tipo_tramite='Consultas temas previsionales/seguros de cesantía')
Respuesta.objects.filter(institucion__nombre_corto='superpensiones', anio=2019, tipo_tramite='2.0').update(tipo_tramite='Certificado de afiliación a una AFP')
Respuesta.objects.filter(institucion__nombre_corto='superpensiones', anio=2019, tipo_tramite='3.0').update(tipo_tramite='Consulta de deuda previsional')
Respuesta.objects.filter(institucion__nombre_corto='superpensiones', anio=2019, tipo_tramite='4.0').update(tipo_tramite='Otros trámites')

Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2019, tipo_tramite='1.0').update(tipo_tramite='Licencias Médicas')
Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2019, tipo_tramite='2.0').update(tipo_tramite='Seguro Laboral')
Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2019, tipo_tramite='3.0').update(tipo_tramite='Otras Materias')

Respuesta.objects.filter(institucion__nombre_corto='supersalud', anio=2019, tipo_tramite='1.0').update(tipo_tramite='Consultas y Tramites de Usuarios')
Respuesta.objects.filter(institucion__nombre_corto='supersalud', anio=2019, tipo_tramite='2.0').update(tipo_tramite='Reclamos contra FONASA, Isapres y Prestadores')
Respuesta.objects.filter(institucion__nombre_corto='supersalud', anio=2019, tipo_tramite='3.0').update(tipo_tramite='Solicitud de inscripción de títulos')

Respuesta.objects.filter(institucion__nombre_corto='capredena', anio=2020, tipo_tramite='1.0').update(tipo_tramite='Pensión')
Respuesta.objects.filter(institucion__nombre_corto='capredena', anio=2020, tipo_tramite='2.0').update(tipo_tramite='Horas médicas')
Respuesta.objects.filter(institucion__nombre_corto='capredena', anio=2020, tipo_tramite='3.0').update(tipo_tramite='Consultas previsionales')
Respuesta.objects.filter(institucion__nombre_corto='capredena', anio=2020, tipo_tramite='4.0').update(tipo_tramite='Certificados')
Respuesta.objects.filter(institucion__nombre_corto='capredena', anio=2020, tipo_tramite='5.0').update(tipo_tramite='Pago beneficios')
Respuesta.objects.filter(institucion__nombre_corto='capredena', anio=2020, tipo_tramite='6.0').update(tipo_tramite='Otros')

Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2020, tipo_tramite='1.0').update(tipo_tramite='Inscripción Atención Primaria')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2020, tipo_tramite='2.0').update(tipo_tramite='Afiliación')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2020, tipo_tramite='3.0').update(tipo_tramite='Venta MLE')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2020, tipo_tramite='4.0').update(tipo_tramite='Certificados')
Respuesta.objects.filter(institucion__nombre_corto='fonasa', anio=2020, tipo_tramite='5.0').update(tipo_tramite='Otros')

Respuesta.objects.filter(institucion__nombre_corto='dipreca', anio=2020, tipo_tramite='1.0').update(tipo_tramite='Zona Norte')
Respuesta.objects.filter(institucion__nombre_corto='dipreca', anio=2020, tipo_tramite='2.0').update(tipo_tramite='Zona Centro')
Respuesta.objects.filter(institucion__nombre_corto='dipreca', anio=2020, tipo_tramite='3.0').update(tipo_tramite='Zona Sur')
Respuesta.objects.filter(institucion__nombre_corto='dipreca', anio=2020, tipo_tramite='4.0').update(tipo_tramite='Metropolitana')


Respuesta.objects.filter(institucion__nombre_corto='isp', anio=2020, tipo_tramite='1.0').update(tipo_tramite='Autorización/Modificaciones')
Respuesta.objects.filter(institucion__nombre_corto='isp', anio=2020, tipo_tramite='2.0').update(tipo_tramite='Realización de ensayos/exámenes/calibraciones')
Respuesta.objects.filter(institucion__nombre_corto='isp', anio=2020, tipo_tramite='3.0').update(tipo_tramite='Gestion de trasplante')
Respuesta.objects.filter(institucion__nombre_corto='isp', anio=2020, tipo_tramite='4.0').update(tipo_tramite='Vigilancia')

Respuesta.objects.filter(institucion__nombre_corto='isl', anio=2020, tipo_tramite='1.0').update(tipo_tramite='Prestaciones médicas')
Respuesta.objects.filter(institucion__nombre_corto='isl', anio=2020, tipo_tramite='2.0').update(tipo_tramite='Prestaciones económicas')
Respuesta.objects.filter(institucion__nombre_corto='isl', anio=2020, tipo_tramite='3.0').update(tipo_tramite='Prevención de riesgos')
Respuesta.objects.filter(institucion__nombre_corto='isl', anio=2020, tipo_tramite='4.0').update(tipo_tramite='Gestión de cotizantes')


Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2020, tipo_tramite='1.0').update(tipo_tramite='Discapacidad')
Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2020, tipo_tramite='2.0').update(tipo_tramite='Estado de Resolución')
Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2020, tipo_tramite='3.0').update(tipo_tramite='Recurso de Reposición')
Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2020, tipo_tramite='4.0').update(tipo_tramite='Ley Sanna')
Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2020, tipo_tramite='5.0').update(tipo_tramite='Apelación Isapre')
Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2020, tipo_tramite='6.0').update(tipo_tramite='Recurso de Reposición Isapre')
Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2020, tipo_tramite='7.0').update(tipo_tramite='Modificación Isapre')
Respuesta.objects.filter(institucion__nombre_corto='saludpublica', anio=2020, tipo_tramite='8.0').update(tipo_tramite='Otros trámites')

Respuesta.objects.filter(institucion__nombre_corto='superpensiones', anio=2020, tipo_tramite='1.0').update(tipo_tramite='Consultas y reclamos (general)')
Respuesta.objects.filter(institucion__nombre_corto='superpensiones', anio=2020, tipo_tramite='2.0').update(tipo_tramite='Consultas y reclamos (10%)')
Respuesta.objects.filter(institucion__nombre_corto='superpensiones', anio=2020, tipo_tramite='3.0').update(tipo_tramite='Certificado de afiliacion a una AFP')
Respuesta.objects.filter(institucion__nombre_corto='superpensiones', anio=2020, tipo_tramite='4.0').update(tipo_tramite='Consulta de afiliados fallecidos con saldo en las cuentas individuales')
Respuesta.objects.filter(institucion__nombre_corto='superpensiones', anio=2020, tipo_tramite='5.0').update(tipo_tramite='Consulta de deuda previsional')
Respuesta.objects.filter(institucion__nombre_corto='superpensiones', anio=2020, tipo_tramite='6.0').update(tipo_tramite='Consulta de potenciales beneficiarios de APS')

Respuesta.objects.filter(institucion__nombre_corto='supersalud', anio=2020, tipo_tramite='1.0').update(tipo_tramite='Consultas y trámites')
Respuesta.objects.filter(institucion__nombre_corto='supersalud', anio=2020, tipo_tramite='2.0').update(tipo_tramite='Reclamos contra FONASA, Isapres y Prestadores')
Respuesta.objects.filter(institucion__nombre_corto='supersalud', anio=2020, tipo_tramite='3.0').update(tipo_tramite='Inscripción RNPI')

Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2020, tipo_tramite='1.0').update(tipo_tramite='Licencias medicas')
Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2020, tipo_tramite='2.0').update(tipo_tramite='Seguridad Laboral')
Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2020, tipo_tramite='3.0').update(tipo_tramite='Creditos sociales')
Respuesta.objects.filter(institucion__nombre_corto='suseso', anio=2020, tipo_tramite='4.0').update(tipo_tramite='Otras Materias')


institucion = Institucion.objects.get(codigo_dipres='1821')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=1, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1822')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=2, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1823')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=3, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1824')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=4, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1825')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=5, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1826')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=6, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1827')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=7, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1828')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=8, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1829')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=9, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1830')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=10, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1831')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=11, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1832')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=12, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1833')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=13, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1834')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=14, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1835')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=15, datos__CANAL='PRESENCIAL').update(institucion=institucion)
institucion = Institucion.objects.get(codigo_dipres='1836')
Respuesta.objects.filter(anio=2020, institucion__nombre_corto='vivienda', datos__region_cf=16, datos__CANAL='PRESENCIAL').update(institucion=institucion)


servius = Institucion.objects.filter(nombre_corto__icontains='serviu')
respuestas = Respuesta.objects.filter(anio=2021, institucion__in=servius)
vivienda = Institucion.objects.get(nombre_corto='vivienda')
for respuesta in respuestas:
    respuesta.pk = None
    respuesta.institucion = vivienda
    respuesta.save()


Respuesta.objects.filter(anio=2021, tipo_tramite='100').update(tipo_tramite='OIRS')
Respuesta.objects.filter(anio=2021, tipo_tramite='200').update(tipo_tramite='BECAS')
Respuesta.objects.filter(anio=2021, tipo_tramite='300').update(tipo_tramite='TNE')
Respuesta.objects.filter(anio=2021, tipo_tramite='400').update(tipo_tramite='ORASMI')
Respuesta.objects.filter(anio=2021, tipo_tramite='500').update(tipo_tramite='FSPR')
Respuesta.objects.filter(anio=2021, tipo_tramite='600').update(tipo_tramite='POSTULACIÓN A JARDINES INFANTILES')
Respuesta.objects.filter(anio=2021, tipo_tramite='700').update(tipo_tramite='CONSULTAS')
Respuesta.objects.filter(anio=2021, tipo_tramite='800').update(tipo_tramite='TRÁMITES')
Respuesta.objects.filter(anio=2021, tipo_tramite='1000').update(tipo_tramite='RECLAMOS')
Respuesta.objects.filter(anio=2021, tipo_tramite='1100').update(tipo_tramite='VISAS')
Respuesta.objects.filter(anio=2021, tipo_tramite='1200').update(tipo_tramite='SOLICITUDES')
Respuesta.objects.filter(anio=2021, tipo_tramite='1300').update(tipo_tramite='OTROS TRAMITES')
Respuesta.objects.filter(anio=2021, tipo_tramite='1400').update(tipo_tramite='IDENTIFICACIÓN')
Respuesta.objects.filter(anio=2021, tipo_tramite='1500').update(tipo_tramite='TRÁMITES RELATIVOS A VEHÍCULOS')
Respuesta.objects.filter(anio=2021, tipo_tramite='1600').update(tipo_tramite='EMISIÓN DE CERTIFICADOS')
Respuesta.objects.filter(anio=2021, tipo_tramite='1700').update(tipo_tramite='MEDIACIÓN FAMILIAR')
Respuesta.objects.filter(anio=2021, tipo_tramite='1800').update(tipo_tramite='TRANSPORTE ESCUCHA')
Respuesta.objects.filter(anio=2021, tipo_tramite='1900').update(tipo_tramite='CONSULTAS Y RECLAMOS')
Respuesta.objects.filter(anio=2021, tipo_tramite='2000').update(tipo_tramite='ESTADO DE RESOLUCIÓN')
Respuesta.objects.filter(anio=2021, tipo_tramite='2100').update(tipo_tramite='MODIFICACIÓN ISAPRE')
Respuesta.objects.filter(anio=2021, tipo_tramite='2200').update(tipo_tramite='RECURSO DE REPOSICIÓN')
Respuesta.objects.filter(anio=2021, tipo_tramite='2300').update(tipo_tramite='DISCAPACIDAD')
Respuesta.objects.filter(anio=2021, tipo_tramite='2400').update(tipo_tramite='APELACIÓN ISAPRE DS3')
Respuesta.objects.filter(anio=2021, tipo_tramite='2500').update(tipo_tramite='RECURSO DE REPOSICIÓN ISAPRE')
Respuesta.objects.filter(anio=2021, tipo_tramite='2600').update(tipo_tramite='LEY SANNA')
Respuesta.objects.filter(anio=2021, tipo_tramite='2700').update(tipo_tramite='CERTIFICADO AFILIACION')
Respuesta.objects.filter(anio=2021, tipo_tramite='2800').update(tipo_tramite='VENTA BONO')
Respuesta.objects.filter(anio=2021, tipo_tramite='2900').update(tipo_tramite='CONSULTAS SEGURO PUBLICO')
Respuesta.objects.filter(anio=2021, tipo_tramite='3000').update(tipo_tramite='AFILIACION')
Respuesta.objects.filter(anio=2021, tipo_tramite='3100').update(tipo_tramite='INSCRIPCION PERCAPITA')
Respuesta.objects.filter(anio=2021, tipo_tramite='3200').update(tipo_tramite='GICONA')
Respuesta.objects.filter(anio=2021, tipo_tramite='3300').update(tipo_tramite='LAB')
Respuesta.objects.filter(anio=2021, tipo_tramite='3400').update(tipo_tramite='SIPRO')
Respuesta.objects.filter(anio=2021, tipo_tramite='3500').update(tipo_tramite='INSCRIPCIÓN EN RNPI')

Respuesta.objects.filter(anio=2021, educacion='#NULL!').update(educacion='99')
Respuesta.objects.filter(anio=2021, educacion='4').update(educacion='99')

Respuesta.objects.filter(anio=2021, sexo='Otra/ Prefiero no responder').update(sexo='99')
Respuesta.objects.filter(anio=2021, sexo='3').update(sexo='99')
Respuesta.objects.filter(anio=2021, sexo='#NULL!').update(sexo='99')

Respuesta.objects.filter(habilitado='1').update(habilitado='No habilitado')
Respuesta.objects.filter(habilitado='2').update(habilitado='Medianamente habilitado')
Respuesta.objects.filter(habilitado='3').update(habilitado='Habilitado')

Respuesta.objects.filter(sexo__in=['99', '3', '3.0', '9.0']).update(sexo='99')


Respuesta.objects.filter(institucion__nombre_corto='cultura', anio=2020, tuvo_problema='3').update(tuvo_problema='88')

Respuesta.objects.filter(institucion__nombre_corto='serviciocivil', anio=2021, tuvo_problema='3').update(tuvo_problema='88')
Respuesta.objects.filter(institucion__nombre_corto='serviciocivil', anio=2021, tuvo_problema='4').update(tuvo_problema='99')


for institucion in Institucion.objects.filter(codigo_dipres__in=['0815', '0601', '0807', '0817', '1001', '1901', '2903']):
    institucion.datos["agrupacion"] = "Ciudadanía /T. Generales"
    institucion.save()

for institucion in Institucion.objects.filter(codigo_dipres__in=['0709', '0716', '0723', '0831', '0801', '1303', '1304']):
    institucion.datos["agrupacion"] = "Economía"
    institucion.save()


for institucion in Institucion.objects.filter(codigo_dipres__in=['0901', '0911', '1401', '2106']):
    institucion.datos["agrupacion"] = "Social"
    institucion.save()


for institucion in Institucion.objects.all():
    anios = [i.get("anio") for i in institucion.respuesta_set.all().distinct('anio').values('anio')]
    institucion.datos["anios"] = anios
    if len(anios) == 0:
        institucion.datos["anios_string"] = None
    if len(anios) == 1:
        institucion.datos["anios_string"] = anios[0]

    if len(anios) > 1:
        institucion.datos["anios_string"] = ", ".join([str(a) for a in anios][0:-1]) + " y " + str(anios[-1])

    institucion.save()

for institucion in Institucion.objects.all():
    institucion.resumen = institucion.calcular_resumen()
    institucion.save()
