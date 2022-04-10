import os
import tempfile
import boto3
from datetime import datetime

from weasyprint import HTML, CSS

try:
    from weasyprint.text.fonts import FontConfiguration
except:
    pass

try:
    from weasyprint.fonts import FontConfiguration
except:
    pass

from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.views.decorators.csrf import csrf_exempt

from portal.models import Carga
from django.template.loader import render_to_string
import hashlib


import pandas as pd
import pyreadstat

from pytz import timezone

from base.models import Institucion
from portal.models import Permiso
import string

import random


def randomString(stringLength):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))


def instituciones(request):
    user = JWTAuthentication().authenticate(request)[0]
    instituciones_ids = Permiso.objects.filter(user=user).values('institucion')
    instituciones = list(Institucion.objects.filter(pk__in=instituciones_ids).values('id', 'nombre', 'datos').order_by('nombre'))
    for institucion in instituciones:
        institucion["tipos_permisos"] = [p.tipo for p in Permiso.objects.filter(user=user, institucion_id=institucion["id"])]

    return JsonResponse(instituciones, safe=False)


from usuarios.models import User


@csrf_exempt
def subir(request, institucion_id=0):

    if institucion_id == 0:
        Institucion.objects.get_or_create(pk=0)

    if request.method != 'POST':
        return

    try:
        user = JWTAuthentication().authenticate(request)[0]
    except:
        user = User.objects.all()[0]

    img = request.FILES.get('archivo')
    session = boto3.Session(
        aws_access_key_id=os.environ.get("CLAVE_AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("CLAVE_AWS_SECRET_ACCESS_KEY"),
    )

    bucket_name = os.environ.get("BUCKET")
    s3 = session.resource('s3')
    random_string = randomString(16)
    name = "{}/{}.{}".format(institucion_id, random_string, img.name.split(".")[-1])
    key = 'cargas2021/{}'.format(name)
    s3.Bucket(bucket_name).put_object(Key=key, Body=img, ACL='public-read')
    url = "https://s3-{}.amazonaws.com/{}/cargas2021/{}".format(os.environ.get("S3_AWS_REGION"), bucket_name, name)

    checksum = hashlib.md5(img.read()).hexdigest()

    data = {'url': url,
            'tipo': request.GET.get("tipo"),
            'checksum': checksum}

    log = {
        'a': 'subido',
        'user': {'id': user.id,
                 #  'nombre_completo': user.username,
                 'username': user.username},
        'fechahora': str(datetime.now()),
    }
    carga = Carga(institucion_id=institucion_id,
                  status='subido',
                  data=data,
                  historial={'logs': [log]})
    carga.save()

    mensajes = None
    data = None
    if request.GET.get("tipo") == 'datos' or institucion_id == 0:
        try:
            resultado_evaluacion, mensajes, data = evaluar(request, carga_id=carga.id)
            carga.data = data
            if resultado_evaluacion:
                log = {'de': 'subido', 'a': 'verificado', 'fechahora': str(datetime.now()), }
                carga.status = 'verificado'
            else:
                log = {'de': 'subido', 'a': 'no verificado', 'mensajes': mensajes, 'fechahora': str(datetime.now()), }
                carga.status = 'no verificado'

        except:
            log = {'de': 'subido', 'a': 'no verificado', 'mensajes': ['No se pudo procesar archivo'], 'fechahora': str(datetime.now()), }
            carga.status = 'no verificado'

        # CFFM
        carga.status = 'verificado'
        carga.historial["logs"].append(log)
        carga.save()

    return JsonResponse({
        "uploaded": True,
        "url": url,
        "carga": carga.id,
        "mensajes": mensajes,
        "data": data
    }
    )


def evaluar(request, carga_id=None):

    mensajes = []
    session = boto3.Session(
        aws_access_key_id=os.environ.get("CLAVE_AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("CLAVE_AWS_SECRET_ACCESS_KEY"),
    )

    carga = Carga.objects.get(pk=carga_id)
    data = carga.data

    bucket_name = os.environ.get("S3_BUCKET_NAME")
    s3 = session.resource('s3')
    s3.Bucket(bucket_name).download_file(carga.data.get("url")[60:], '/tmp/data.sav')

    df, meta = pyreadstat.read_sav('/tmp/data.sav')

    columnas = [
        {
            'nombre': 'Canal',
            'requerida': True,
            'valores': [1, 2, 3]
        },
        {
            'nombre': 'Región',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 88, 99]
        },

        {
            'nombre': 'PI1',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 88, 99]
        },
        {
            'nombre': 'PI2',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PI3_1',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PI3_2',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PI3_3',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PI3_4',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PI3_5',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PI3_6',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEX01 CF',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEX02',
            'requerida': True,
        },
        {
            'nombre': 'PEC06_01 CF'
        },
        {
            'nombre': 'PEC06_02 CF'
        },
        {
            'nombre': 'PEC07',
        },
        {
            'nombre': 'PEX03_1',

        },
        {
            'nombre': 'PI3_1',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEX04',
            'requerida': True,
            'valores': [1, 2, 3, 4, 88, 99]
        },
        {
            'nombre': 'PEX05',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEX06',
            'requerida': True
        },
        {
            'nombre': 'PEX07_1',
        },
        {
            'nombre': 'PEX07_2',

        },
        {
            'nombre': 'PEC02',
            'requerida': False,
            'valores': [1, 2, 88, 99]
        },
        {
            'nombre': 'PEC03',
            'requerida': False,
            'valores': [1, 2, 3, 4, 88, 99]
        },
        {
            'nombre': 'PEC04_1',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEC04_2',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEC04_3',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEC04_4',
            'requerida': False,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEC04_5',
            'requerida': False,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEC04_6',
            'requerida': False,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEC05_1',
            'requerida': False,
            'valores': [1, 2, 88, 99]
        },
        {
            'nombre': 'PEC05_2',
            'requerida': False,
            'valores': [1, 2, 88, 99]
        },
        {
            'nombre': 'PEC05_3',
            'requerida': False,
            'valores': [1, 2, 88, 99]
        },
        {
            'nombre': 'PEC05_4',
            'requerida': False,
            'valores': [1, 2, 88, 99]
        },
        {
            'nombre': 'PEV01_1',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 88, 99]
        },
        {
            'nombre': 'PEV01_2',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 88, 99]
        },
        {
            'nombre': 'PEV01_1',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEV01_2',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEV01_3',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEV01_4',
            'requerida': False,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEV01_5',
            'requerida': False,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEV01_6',
            'requerida': False,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEV01_7',
            'requerida': False,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEV01_8',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEV01_9',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PDE01',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 88, 99]
        },
        {
            'nombre': 'PDE02',
            'requerida': True,
            'regla': 'exisitr PEX02',
            'valores': [1, 2, 3, 88, 99]
        },
        {
            'nombre': 'PED03',
            'requerida': True
        },
        {
            'nombre': 'PH01_1',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PH01_2',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PH01_3',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PH01_4',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PEP01',
            'requerida': True,
            'valores': [1, 2, 88, 99]
        },
        {
            'nombre': 'PEP03',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 88, 99]
        },
        {
            'nombre': 'PDE04_1',
            'requerida': False,
        },
        {
            'nombre': 'U2',
            'requerida': True,
            'valores': [1, 2, 3]
        },
        {
            'nombre': 'U3',
            'requerida': True,
            'valores': 'integer'
        },
        {
            'nombre': 'UN4',
            'requerida': False,
        },
        {
            'nombre': 'UN5',
        },
        {
            'nombre': 'UN6_1',
            'requerida': False,
            'valores': [1, 2, 88]
        },
        {
            'nombre': 'UN6_2',
            'requerida': False,
            'valores': [1, 2, 88, 99]
        },
        {
            'nombre': 'UN7',
            'requerida': True,
            'valores': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 88, 99]
        }
    ]

    for columna in columnas:
        existe = False
        for df_c in df.columns:
            if df_c.lower() == columna.get("nombre").lower():
                existe = True
                break

        if not existe:
            mensajes.append('Columna {} no está en el archivo'.format(columna.get("nombre")))

        valores = columna.get("valores")
        if valores:
            if valores == 'integer':
                continue
            try:
                df[~df["PI2"].isin(valores)]["PI2"]
            except:
                import ipdb
                ipdb.set_trace()
            if len(df[~df["PI2"].isin(valores)]["PI2"]) > 0:
                mensajes.append('Columna {} no admite valores {}'.format(columna.get("nombre"), df[~df["PI2"].isin(valores)]["PI2"].drop_duplicates().tolist()))

    # if len(mensajes) > 0:
    #     return False, mensajes, data

    data["cantidad_registros"] = df.shape[0]
    positivo = sum(df[(df["PI2"] >= 6) & (df["PI2"] <= 7)]["F_POND"])
    negativo = sum(df[df["PI2"] <= 4]["F_POND"])
    denominador = sum(df[df["PI2"] <= 7]["F_POND"])

    if denominador > 0:
        data["evaluacion_institucion"] = float(positivo - negativo) / denominador
        data["evaluacion_institucion_positivo"] = round(float(positivo / denominador) * 100, 0)
        data["evaluacion_institucion_negativo"] = round(float(negativo / denominador) * 100, 0)
        data["evaluacion_institucion_porcentaje"] = round(float(positivo / denominador) * 100, 0) - round(float(negativo / denominador) * 100, 0)
    else:
        mensajes.append('Ponderador no es > 0')
        return False, mensajes, data

    positivo = sum(df[(df["PEX05"] >= 6) & (df["PEX05"] <= 7)]["F_POND"])
    negativo = sum(df[df["PEX05"] <= 4]["F_POND"])
    denominador = sum(df[df["PEX05"] <= 7]["F_POND"])

    data["satisfaccion_neta"] = float(positivo - negativo) / denominador
    data["satisfaccion_neta_positivo"] = round(float(positivo / denominador) * 100, 0)
    data["satisfaccion_neta_negativo"] = round(float(negativo / denominador) * 100, 0)
    data["satisfaccion_neta_porcentaje"] = round(float(positivo / denominador) * 100, 0) - round(float(negativo / denominador) * 100, 0)

    data["calculado"] = str(datetime.now())

    return True, mensajes, data


def procesar_todos():
    for carga in Carga.objects.filter(pk__in=[195, 191]).order_by('-id'):
        if carga.status not in ['verificado', 'aprobado']:
            continue
        print(carga.status)
        print(carga.id)
        resultado_evaluacion, mensajes, data = evaluar("", carga_id=carga.id)
        # try:
        # except:
        #     continue

        if resultado_evaluacion is False:
            continue

        carga.data = data
        carga.save()


def descarga(request, carga_id=None):
    carga = Carga.objects.get(pk=carga_id)
    session = boto3.Session(
        aws_access_key_id=os.environ.get("CLAVE_AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("CLAVE_AWS_SECRET_ACCESS_KEY"),
    )
    carga = Carga.objects.get(pk=carga_id)
    data = carga.data
    nombre_archivo = data.get("url").split('/')[-1]
    filepath = '/tmp/{}'.format(nombre_archivo)

    bucket_name = os.environ.get("S3_BUCKET_NAME")

    s3 = session.resource('s3')
    s3.Bucket(bucket_name).download_file(carga.data.get("url")[66:], filepath)

    import magic
    mime = magic.Magic(mime=True)

    with open(filepath, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type=mime.from_file(filepath))
        response['Content-Disposition'] = 'inline; filename={}'.format(nombre_archivo)
        response['Content-Transfer-Encoding'] = 'binary'
        return response


def pdf_dato(request, carga_id=None):
    carga = Carga.objects.get(pk=carga_id)
    nombre_archivo = "informe_carga_dato_{}".format(carga.institucion.id)

    context = {
        'carga': carga,
        'static_url': os.getcwd(),
    }
    context["aprobado"] = datetime.strptime([i for i in carga.historial.get("logs") if i.get("a") == 'aprobado'][-1].get("fechahora")[0:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone('UTC'))
    context["subido"] = datetime.strptime([i for i in carga.historial.get("logs") if i.get("a") == 'subido'][-1].get("fechahora")[0:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone('UTC'))
    context["now"] = datetime.now()

    html_string = render_to_string('satisfaccion/dato.html', context)

    html = HTML(string=html_string, base_url=os.getcwd() + "/media")

    # font_config = FontConfiguration()
    # css = CSS(string='''
    # @font-face {
    #     font-family: Robotos;
    #     src: url(https://fonts.googleapis.com/css?family=Roboto);
    # }
    # ''', font_config=font_config)

    # result = html.write_pdf(stylesheets=[css, 'portal/templates/satisfaccion/informe.css'])
    result = html.write_pdf(stylesheets=['portal/templates/satisfaccion/informe.css'])

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename="%s.pdf"' % (nombre_archivo)
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def pdf_presentacion(request, carga_id=None):
    carga = Carga.objects.get(pk=carga_id)
    nombre_archivo = "certificado_final_{}".format(carga.institucion.id)

    context = {
        'carga': carga,
        'static_url': os.getcwd(),
    }
    context["aprobado"] = datetime.strptime([i for i in carga.historial.get("logs") if i.get("a") == 'aprobado'][-1].get("fechahora")[0:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone('UTC'))
    context["subido"] = datetime.strptime([i for i in carga.historial.get("logs") if i.get("a") == 'subido'][-1].get("fechahora")[0:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone('UTC'))
    context["now"] = datetime.now()

    # if carga.service_id in [9, 112, 79, 34, 171, 161]:
    #     html_string = render_to_string('satisfaccion/presentacion_alternativa.html', context)
    # elif carga.service_id in [154]:
    #     html_string = render_to_string('satisfaccion/presentacion_senama.html', context)
    # else:
    html_string = render_to_string('satisfaccion/presentacion.html', context)

    html = HTML(string=html_string, base_url=os.getcwd() + "/media")

    # font_config = FontConfiguration()
    # css = CSS(string='''
    # @font-face {
    #     font-family: Roboto;
    #     src: url(https://fonts.googleapis.com/css?family=Roboto);
    # }
    # ''', font_config=font_config)

    # result = html.write_pdf(
    #     stylesheets=[css, 'portal/templates/satisfaccion/informe.css'])

    result = html.write_pdf(stylesheets=['portal/templates/satisfaccion/informe.css'])

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename="%s.pdf"' % (nombre_archivo)
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def excel(request):
    nombre_archivo = "resumen.xls"
    wb = xlwt.Workbook(encoding='utf-8')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % (nombre_archivo)

    ws = wb.add_sheet("Resumen")
    ws.write(0, 0, 'Servicio')
    ws.write(0, 1, 'Datos')
    ws.write(0, 2, 'Presentacion')
    ws.write(0, 3, 'Positivo')
    ws.write(0, 4, 'Negativo')
    ws.write(0, 5, 'Satisfaccion')

    services = Service.objects.filter(pk__in=Carga.objects.all().values('service_id')).order_by('code')

    for row_num, service in enumerate(services, start=1):
        ws.write(row_num, 0, service.name)

        # datos
        carga = Carga.objects.filter(data__tipo='datos', service=service, status='aprobado').first()
        if carga is None:
            carga = Carga.objects.filter(data__tipo='datos', service=service, status='verificado').first()

        ws.write(row_num, 1, carga.status if carga else None)
        if carga:
            ws.write(row_num, 3, carga.data.get("satisfaccion_neta_positivo"))
            ws.write(row_num, 4, carga.data.get("satisfaccion_neta_negativo"))
            ws.write(row_num, 5, carga.data.get("satisfaccion_neta_porcentaje"))

        # informe
        carga = Carga.objects.filter(data__tipo='presentacion', service=service, status='aprobado').first()
        if carga is None:
            carga = Carga.objects.filter(data__tipo='presentacion', service=service, status='subido').first()
        ws.write(row_num, 2, carga.status if carga else None)

    wb.save(response)
    return response


# def prueba(request):
#     producto_agregado = self.agregar_producto(request)
#     caso = self.get_object()

#     img = request.FILES.get('file')
#     session = boto3.Session(
#         aws_access_key_id=os.environ.get("CLAVE_AWS_ACCESS_KEY_ID"),
#         aws_secret_access_key=os.environ.get("CLAVE_AWS_SECRET_ACCESS_KEY"),
#     )
#     bucket_name = os.environ.get("BUCKET")
#     bucket_url = os.environ.get("BUCKET_URL")
#     s3 = session.resource('s3')

#     key = 'archivos-2022-testing/{}/{}.{}'.format(caso.id, randomString(16), img.name.split(".")[-1])

#     s3.Bucket(bucket_name).put_object(Key=key, Body=img, ACL='public-read')
#     url = "{}/{}".format(bucket_url, key)

#     # found = False

#     productos = caso.detalle.get("productos", [])
#     for producto in productos:
#         if producto.get("codigo") != producto_agregado.get("codigo"):
#             continue

#         producto["prescripcion_tipo"] = 'adjuntar'
#         producto["documentacion"] = producto.get("documentacion") or Catalogo.objects.get(pk=producto.get("productoId")).informacion.get("documentacion")
#         for documentacion in producto["documentacion"]:
#             if documentacion.get("formulario") != request.GET.get("documentacionFormulario"):
#                 continue
#             documentacion["imagen"] = {
#                 "url": url,
#                 "agregada": str(datetime.now())
#             }

#     caso.detalle["productos"] = productos
#     caso.save()
#     serializer = self.get_serializer(caso)
#     return Response(serializer.data)
