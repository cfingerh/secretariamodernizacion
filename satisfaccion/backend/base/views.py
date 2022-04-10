from django.db import connections
from django.http import JsonResponse
from base.models import Institucion, Respuesta
from django.db.models import Sum

from datetime import datetime


def informe(request, codigo_dipres):
    return JsonResponse({'url': 'asd'})


def canal_preferencia(request, pk=None):

    respuestas = Respuesta.objects.all()
    anio = 2020

    if pk:
        institucion = Institucion.objects.get(pk=pk)
        respuestas = respuestas.filter(institucion=institucion)
        anio = institucion.datos.get("anios")[-1]

    # labels = ['pec_canal_telefono', 'pec_canal_web', 'pec_canal_presencial']
    # MK recomendó ocupar pec_Eval los que tengan dato en vez que pec_Canal
    labels = ['pec_eval_telefono', 'pec_eval_web', 'pec_eval_presencial']

    data = []
    labels_with_data = []
    resp_anio = respuestas.filter(anio=anio)
    total = resp_anio.count()
    for label in labels:
        porcentaje = round(resp_anio.filter(**{label + '__isnull': False}).count() / total * 100, 0)
        if porcentaje > 0:
            labels_with_data.append(label)
            data.append(porcentaje)

    return JsonResponse({'labels': labels_with_data, 'data': data}, safe=False)


def canal_evaluacion(request, pk=None):

    respuestas = Respuesta.objects.all()
    anio = 2020

    if pk:
        institucion = Institucion.objects.get(pk=pk)
        respuestas = respuestas.filter(institucion=institucion)
        anio = institucion.datos.get("anios")[-1]

    labels = ['pec_eval_telefono', 'pec_eval_web', 'pec_eval_presencial']
    # labels = ['pec_eval_telefono']

    data = {
        'insatisfecho': [],
        'neutro': [],
        'satisfecho': []
    }

    anios = ["2016", "2017", "2018", "2019", "2020"]

    datasets = []
    for anio in anios:
        resp_anio = respuestas.filter(anio=anio)
        if resp_anio.count() == 0:
            continue

        datasets.append({'label': 'Satisfecho', 'data': [], 'stack': anio, 'backgroundColor': '#00d1b2', })
        datasets.append({'label': 'Neutro', 'data': [], 'stack': anio, 'backgroundColor': '#FBD561', })
        datasets.append({'label': 'Insatisfecho', 'data': [], 'stack': anio, 'backgroundColor': '#F08289', })

        for label in labels:
            insatisfecho_sum = resp_anio.filter(**{label + '__in': [1, 2, 3, 4]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
            neutro_sum = resp_anio.filter(**{label + '__in': [5]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
            satisfecho_sum = resp_anio.filter(**{label + '__in': [6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
            otros_sum = resp_anio.exclude(**{label + '__in': [1, 2, 3, 4, 5, 6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
            total = insatisfecho_sum + neutro_sum + satisfecho_sum + otros_sum

            # if total and total >= 0:
            #     labels_with_data.append(label)
            for dataset in datasets:
                if dataset.get("label") == 'Satisfecho' and dataset.get("stack") == anio:
                    dataset["data"].append(round(satisfecho_sum / total * 100))

            for dataset in datasets:
                if dataset.get("label") == 'Neutro' and dataset.get("stack") == anio:
                    dataset["data"].append(round(neutro_sum / total * 100))

            for dataset in datasets:
                if dataset.get("label") == 'Insatisfecho' and dataset.get("stack") == anio:
                    dataset["data"].append(round(insatisfecho_sum / total * 100))

        print(datasets)

    if len(datasets) > 6:
        datasets = datasets[-6:]

    return JsonResponse({'labels': labels, 'datasets': datasets}, safe=False)


def data_atributos(request, pk=None):
    print(datetime.now())
    respuestas = Respuesta.objects.all()
    anio = 2021

    if pk:
        institucion = Institucion.objects.get(pk=pk)
        respuestas = respuestas.filter(institucion=institucion)
        anio = institucion.datos.get("anios")[-1]

    labels = ['pev_tram_facil', 'pev_tram_tiempo', 'pev_tram_claridad_pasos', 'pev_tram_info_compr',
              'pev_tram_info_util', 'pev_tram_resp_util', 'pev_tram_resp_compl', 'pev_tram_resp_clara', 'pev_tram_acogido', ]

    data = {
        'insatisfecho': [],
        'neutro': [],
        'satisfecho': []
    }

    efectivo_para_ordenar = []
    labels_with_data = []
    resp_anio = respuestas.filter(anio=anio)
    for label in labels:
        insatisfecho_sum = resp_anio.filter(**{label + '__in': [1, 2, 3, 4]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        neutro_sum = resp_anio.filter(**{label + '__in': [5]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        satisfecho_sum = resp_anio.filter(**{label + '__in': [6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0

        otros_sum = resp_anio.exclude(**{label + '__in': [1, 2, 3, 4, 5, 6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        total = insatisfecho_sum + neutro_sum + satisfecho_sum + otros_sum

        if total and total >= 0:
            labels_with_data.append(label)
            data["insatisfecho"].append(round(insatisfecho_sum / total * 100))
            data["neutro"].append(round(neutro_sum / total * 100))
            data["satisfecho"].append(round(satisfecho_sum / total * 100))
            efectivo_para_ordenar.append(round(satisfecho_sum / total * 100) - round(insatisfecho_sum / total * 100))

    ordenado = sorted(range(len(efectivo_para_ordenar)), key=lambda k: efectivo_para_ordenar[k])
    labels_with_data = ordenar(labels_with_data, ordenado)
    data["insatisfecho"] = ordenar(data["insatisfecho"], ordenado)
    data["neutro"] = ordenar(data["neutro"], ordenado)
    data["satisfecho"] = ordenar(data["satisfecho"], ordenado)

    return JsonResponse({'labels': labels_with_data, 'data': data}, safe=False)


import copy


def ordenar(arreglo, ordenado):
    temp = copy.deepcopy(arreglo)
    for (i, v) in enumerate(ordenado):
        temp[i] = arreglo[v]

    return temp


def data_imagen(request, pk=None):
    respuestas = Respuesta.objects.all()
    anio = 2021

    if pk:
        institucion = Institucion.objects.get(pk=pk)
        respuestas = respuestas.filter(institucion=institucion)
        anio = institucion.datos.get("anios")[-1]

    labels = ['pi_imagen_transp', 'pi_imagen_preocupa', 'pi_imagen_actual', 'pi_imagen_funcion', 'pi_imagen_satisface']

    data = {
        'insatisfecho': [],
        'neutro': [],
        'satisfecho': []
    }

    resp_anio = respuestas.filter(anio=anio)
    labels_with_data = []
    efectivo_para_ordenar = []
    for label in labels:
        insatisfecho_sum = resp_anio.filter(**{label + '__in': [1, 2, 3, 4]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        neutro_sum = resp_anio.filter(**{label + '__in': [5]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        satisfecho_sum = resp_anio.filter(**{label + '__in': [6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0

        otros_sum = resp_anio.exclude(**{label + '__in': [1, 2, 3, 4, 5, 6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        total = insatisfecho_sum + neutro_sum + satisfecho_sum + otros_sum

        if total and total >= 0:
            labels_with_data.append(label)
            data["insatisfecho"].append(round(insatisfecho_sum / total * 100))
            data["neutro"].append(round(neutro_sum / total * 100))
            data["satisfecho"].append(round(satisfecho_sum / total * 100))
            efectivo_para_ordenar.append(round(satisfecho_sum / total * 100) - round(insatisfecho_sum / total * 100))

    ordenado = sorted(range(len(efectivo_para_ordenar)), key=lambda k: efectivo_para_ordenar[k])
    labels_with_data = ordenar(labels_with_data, ordenado)
    data["insatisfecho"] = ordenar(data["insatisfecho"], ordenado)
    data["neutro"] = ordenar(data["neutro"], ordenado)
    data["satisfecho"] = ordenar(data["satisfecho"], ordenado)

    return JsonResponse({'labels': labels_with_data, 'data': data}, safe=False)


def getColor(dimension):
    # https://learnui.design/tools/data-color-picker.html
    if dimension == 'Hombre':
        return '#003f5c'
    if dimension == 'Mujer':
        return ' #bc5090'

    if dimension == 'Habilitado':
        return '#003f5c'
    if dimension == 'Medianamente habilitado':
        return ' #bc5090'
    if dimension == 'No habilitado':
        return '#ffa600'

    if dimension == '18 a 34 años':
        return '#003f5c'
    if dimension == '35 a 44 años':
        return ' #58508d'
    if dimension == '45 a 54 años':
        return '#bc5090'
    if dimension == '55 años o más':
        return '#ff6361'

    if dimension == 'Superior':
        return '#003f5c'
    if dimension == 'Enseñanza Media':
        return ' #bc5090'
    if dimension == 'Enseñanza Básica':
        return '#ffa600'

    print(dimension)
    return dimension


def data_dimension_anio(request, pk=None):
    respuestas = Respuesta.objects.all()

    if pk:
        institucion = Institucion.objects.get(codigo_dipres=pk)
        respuestas = respuestas.filter(institucion=institucion)
    else:
        vivienda = Institucion.objects.get(nombre_corto='vivienda')
        respuestas = respuestas.exclude(institucion=vivienda, anio=2021)

    medicion = request.GET.get("medicion", 'experiencia')

    dimension_nombre = request.GET.get("dimension", 'sexo')

    labels = [a["anio"] for a in respuestas.distinct('anio').order_by('anio').values('anio')]
    # labels = [2015, 2016, 2017, 2018, 2019, 2020, 2021]

    dimensiones = [d[dimension_nombre] for d in respuestas.values(dimension_nombre).distinct(dimension_nombre) if d[dimension_nombre] and d[dimension_nombre] not in ['88', '99']]

    # data = {
    #     'insatisfecho': [],
    #     'neutro': [],
    #     'satisfecho': []
    # }
    labels_with_data = []

    datasets = []
    agrupados = respuestas.values(medicion, dimension_nombre, 'anio').order_by(medicion, dimension_nombre, 'anio').annotate(suma=Sum('f_pond'))
    for dimension in dimensiones:
        dataset_data = []
        for label in labels:
            neutro_sum = sum([a.get("suma") for a in agrupados if a.get(dimension_nombre) == dimension and a.get('anio') == label and a.get(medicion) in [5]])
            satisfecho_sum = sum([a.get("suma") for a in agrupados if a.get(dimension_nombre) == dimension and a.get('anio') == label and a.get(medicion) in [6, 7]])
            insatisfecho_sum = sum([a.get("suma") for a in agrupados if a.get(dimension_nombre) == dimension and a.get('anio') == label and a.get(medicion) in [1, 2, 3, 4]])
            otros_sum = sum([a.get("suma") for a in agrupados if a.get(dimension_nombre) == dimension and a.get('anio') == label and a.get(medicion) not in [1, 2, 3, 4, 5, 6, 7]])
            total = insatisfecho_sum + neutro_sum + satisfecho_sum + otros_sum
            if total > 0:
                valor = round(satisfecho_sum / total * 100) - round(insatisfecho_sum / total * 100)
            else:
                valor = None
            dataset_data.append(valor)

        dataset = {"label": dimension,
                   "data": dataset_data,
                   "color": getColor(dimension),
                   "fill": False,
                   "spanGaps": True,
                   }
        datasets.append(dataset)

    labels_con_datos = []
    datasets_con_datos = []
    tiene_datos = []
    for index, anio in enumerate(labels):
        has_datos = False
        for dataset in datasets:
            print(dataset["data"][index])
            if dataset["data"][index]:
                has_datos = True
        tiene_datos.append(has_datos)

    print(tiene_datos)
    from itertools import compress
    labels = list(compress(labels, tiene_datos))
    for dataset in datasets:
        dataset["data"] = list(compress(dataset["data"], tiene_datos))
        if len(dataset["data"]) == 1:
            dataset["backgroundColor"] = dataset["color"]
        else:
            dataset["borderColor"] = dataset["color"]

    return JsonResponse({'labels': labels, 'datasets': datasets}, safe=False)


def data_dimension(request, pk=None):
    respuestas = Respuesta.objects.all()  # .filter(sexo__in=['Hombre', 'Mujer']).filter(educacion__in=['Enseñanza Básica', 'Enseñanza Media', 'Superior'])

    if pk:
        institucion = Institucion.objects.get(pk=pk)
        respuestas = respuestas.filter(institucion=institucion)

    medicion = request.GET.get("medicion", 'experiencia')

    # esto debería salir
    if medicion == 'tipo_tramite':
        medicion = 'experiencia'

    dimension = request.GET.get("dimension", 'anio')
    labels = [d[dimension] for d in respuestas.values(dimension).distinct(dimension) if d[dimension] and d[dimension] not in ['88', '99']]
    if dimension == 'tipo_tramite':
        labels = [l for l in labels if l != 'Otros']

    labels.append('Todos')

    if request.GET.get("edad"):
        respuestas = respuestas.filter(edad=request.GET.get("edad").replace("_", " "))

    if request.GET.get("sexo"):
        respuestas = respuestas.filter(sexo=request.GET.get("sexo"))

    if request.GET.get("educacion"):
        respuestas = respuestas.filter(educacion=request.GET.get("educacion"))

    if request.GET.get("habilitado"):
        respuestas = respuestas.filter(habilitado=request.GET.get("habilitado"))

    if request.GET.get("anio"):
        respuestas = respuestas.filter(anio=request.GET.get("anio"))

    data = {
        'insatisfecho': [],
        'neutro': [],
        'satisfecho': []
    }
    labels_with_data = []

    agrupados = respuestas.values(medicion, dimension).order_by(medicion, dimension).annotate(suma=Sum('f_pond'))
    for label in labels:
        if label == 'Todos':
            insatisfecho_sum = sum([a.get("suma") for a in agrupados if a.get(medicion) in [1, 2, 3, 4]])
            neutro_sum = sum([a.get("suma") for a in agrupados if a.get(medicion) in [5]])
            satisfecho_sum = sum([a.get("suma") for a in agrupados if a.get(medicion) in [6, 7]])
            otros_sum = sum([a.get("suma") for a in agrupados if a.get(medicion) not in [1, 2, 3, 4, 5, 6, 7]])

        else:
            insatisfecho_sum = sum([a.get("suma") for a in agrupados if a.get(dimension) == label and a.get(medicion) in [1, 2, 3, 4]])
            neutro_sum = sum([a.get("suma") for a in agrupados if a.get(dimension) == label and a.get(medicion) in [5]])
            satisfecho_sum = sum([a.get("suma") for a in agrupados if a.get(dimension) == label and a.get(medicion) in [6, 7]])
            otros_sum = sum([a.get("suma") for a in agrupados if a.get(dimension) == label and a.get(medicion) not in [1, 2, 3, 4, 5, 6, 7]])

        total = insatisfecho_sum + neutro_sum + satisfecho_sum + otros_sum

        if total > 0:
            labels_with_data.append(label)

            data["insatisfecho"].append(round(insatisfecho_sum / total * 100))
            data["neutro"].append(round(neutro_sum / total * 100))
            data["satisfecho"].append(round(satisfecho_sum / total * 100))

    return JsonResponse({'labels': labels_with_data, 'data': data}, safe=False)


def data_grafica(request, pk=None):
    print(datetime.now())
    respuestas = Respuesta.objects.all()

    if pk:
        institucion = Institucion.objects.get(codigo_dipres=pk)
        respuestas = respuestas.filter(institucion=institucion)
        anios = institucion.datos.get("anios")
    else:
        anios = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
        vivienda = Institucion.objects.get(nombre_corto='vivienda')
        respuestas = respuestas.exclude(institucion=vivienda, anio=2021)

    medicion = request.GET.get("medicion", 'experiencia')

    if request.GET.get("edad"):
        respuestas = respuestas.filter(edad=request.GET.get("edad").replace("_", " "))

    if request.GET.get("sexo"):
        respuestas = respuestas.filter(sexo=request.GET.get("sexo"))

    if request.GET.get("educacion"):
        respuestas = respuestas.filter(educacion=request.GET.get("educacion"))

    if request.GET.get("habilitado"):
        respuestas = respuestas.filter(habilitado=request.GET.get("habilitado"))

    if request.GET.get("institucion__codigo_dipres"):
        respuestas = respuestas.filter(institucion__codigo_dipres=request.GET.get("institucion__codigo_dipres"))

    data = {
        'insatisfecho': [],
        'neutro': [],
        'satisfecho': []
    }

    resp_anio = respuestas
    agrupados = resp_anio.values(medicion, 'anio').order_by(medicion, 'anio').annotate(suma=Sum('f_pond'))
    for anio in anios:
        insatisfecho_sum = sum([a.get("suma") for a in agrupados if a["anio"] == anio and a.get(medicion) in [1, 2, 3, 4]])
        neutro_sum = sum([a.get("suma") for a in agrupados if a["anio"] == anio and a.get(medicion) in [5]])
        satisfecho_sum = sum([a.get("suma") for a in agrupados if a["anio"] == anio and a.get(medicion) in [6, 7]])
        otros_sum = sum([a.get("suma") for a in agrupados if a["anio"] == anio and a.get(medicion) not in [1, 2, 3, 4, 5, 6, 7]])

        # insatisfecho_sum = resp_anio.filter(**{medicion + '__in': [1, 2, 3, 4]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        # neutro_sum = resp_anio.filter(**{medicion + '__in': [5]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        # satisfecho_sum = resp_anio.filter(**{medicion + '__in': [6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        # otros_sum = resp_anio.exclude(**{medicion + '__in': [1, 2, 3, 4, 5, 6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0

        total = insatisfecho_sum + neutro_sum + satisfecho_sum + otros_sum
        if total == 0:
            data["insatisfecho"].append(None)
            data["neutro"].append(None)
            data["satisfecho"].append(None)
        else:
            data["insatisfecho"].append(round(insatisfecho_sum / total * 100))
            data["neutro"].append(round(neutro_sum / total * 100))
            data["satisfecho"].append(round(satisfecho_sum / total * 100))

    return JsonResponse({'labels': anios, 'data': data}, safe=False)


def resumen(request):
    datos = []
    for institucion in Institucion.objects.all():
        dato = {'nombre': institucion.nombre or institucion.datos.get("codigo")}
        for anio in [2015, 2016, 2017, 2018, 2019, 2020, 2021]:
            respuestas = Respuesta.objects.filter(anio=anio, institucion=institucion)
            if respuestas.count() == 0:
                continue

            dato[anio] = get_valores(respuestas, 'eval_inst')["neta"]
        datos.append(dato)

    return JsonResponse(datos, safe=False)


def get_valores(respuestas, medicion):
    negativo_suma = respuestas.filter(**{'{}__in'.format(medicion): [1, 2, 3, 4]}).aggregate(suma=Sum('f_pond'))["suma"] or 0
    positivo_suma = respuestas.filter(**{'{}__in'.format(medicion): [6, 7]}).aggregate(suma=Sum('f_pond'))["suma"] or 0
    neutro_suma = respuestas.filter(**{'{}__in'.format(medicion): [5]}).aggregate(suma=Sum('f_pond'))["suma"] or 0

    suma = respuestas.filter().aggregate(suma=Sum('f_pond'))["suma"] or 0

    if suma is not None and suma > 0:
        positivo = round((positivo_suma) / suma * 100, 0)
        negativo = round((negativo_suma) / suma * 100, 0)
        neutro = round((neutro_suma) / suma * 100, 0)
    else:
        positivo = 0
        negativo = 0
        neutro = 0

    neta = positivo - negativo
    return {
        'negativo_suma': negativo_suma,
        'negativo_suma': negativo_suma,
        'neutro_suma': neutro_suma,
        'suma': suma,
        'neta': neta,
        'positivo': positivo,
        'negativo': negativo,
        'neutro': neutro,

    }
