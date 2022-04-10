import requests
from load import *
from base.models import Institucion

NOMBRES = [
    {"Instituto de Desarrollo Agropecuario": "2565287"},
    {"Servicio Agrícola y Ganadero": "2565880"},
    {"Subsecretaría de Bienes Nacionales": "2565657"},
    {"Corporación Nacional de Desarrollo Indígena": "2565691"},
    {"Fondo de Solidaridad e Inversion Social": "2565397"},
    {"Servicio Nacional del Adulto Mayor": "2565847"},
    {"Subsecretaría de Servicios Sociales": "2566213"},
    {"Instituto Nacional de Estadísticas": "2566198"},
    {"Instituto Nacional de Propiedad Industrial": "2565333"},
    {"Servicio de Cooperación Técnica": "2565223"},
    {"Servicio Nacional de Pesca y Acuicultura": "2565926"},
    {"Servicio Nacional de Turismo": "2565889"},
    {"Servicio Nacional del Consumidor": "2565518"},
    {"Subsecretaría de Economía y Empresas de Menor Tamaño": "2565209"},
    {"Junta Nacional de Auxilio Escolar y Becas": "2565751"},
    {"Junta Nacional de Jardines Infantiles": "2565773"},
    {"Subsecretaría de Educación": "2565461"},
    {"Superintendencia de Electricidad y Combustibles": "2566073"},
    {"Comisión para el Mercado Financiero": "2567480"},
    {"Dirección de Compras y Contratación Pública": "2565828"},
    {"Dirección Nacional del Servicio Civil": "2566255"},
    {"Servicio de Tesorerías": "2565202"},
    {"Servicio Nacional de Aduanas": "2565700"},
    {"Subsecretaría de Justicia": "2565255"},
    {"Servicio de Registro Civil e Identificación": "2566093"},
    {"Servicio Nacional del Patrimonio Archivo Nacional": "2566209"},
    {"Subsecretaría de Relaciones Exteriores": "2567367"},
    {"Fondo Nacional de Salud": "2565306"},
    {"Instituto de Salud Pública": "2565992"},
    {"Subsecretaría de Salud Pública (COMPIN)": "2565464"},
    {"Superintendencia de Salud": "2565718"},
    {"Subsecretaría de Transportes": "2566193"},
    {"SERVIU Región de Antofagasta": "2566223"},
    {"SERVIU Región de Arica y Parinacota": "2566135"},
    {"SERVIU Región de Atacama": "2567255"},
    {"SERVIU Región de Aysén del Gral. Carlos Ibáñez del Campo": "2566238"},
    {"SERVIU Región de Coquimbo": "2567197"},
    {"SERVIU Región de la Araucanía": "2565362"},
    {"SERVIU Región de Los Lagos": "2567252"},
    {"SERVIU Región de Los Ríos": "2567243"},
    {"SERVIU Región de Magallanes y Antártica Chilena": "2566153"},
    {"SERVIU Región de Ñuble": "2566179"},
    {"SERVIU Región de Tarapacá": "2567229"},
    {"SERVIU Región de Valparaíso": "2566276"},
    {"SERVIU Región del Biobío": "2566168"},
    {"SERVIU Región del Libertador General Bernardo O'Higgins": "2566125"},
    {"SERVIU Región del Maule": "2565420"},
    {"SERVIU Región Metropolitana": "2567200"},
    {"Subsecretaría de Vivienda y Urbanismo": "2566172"},
    {"Subsecretaría del Interior": "2565282"},
    {"Caja de Previsión de la Defensa Nacional": "2565441"},
    {"Dirección de Previsión de Carabineros de Chile": "2565402"},
    {"Dirección del Trabajo": "2565820"},
    {"Dirección General de Crédito Prendario": "2565641"},
    {"Instituo de Previsión Social": "2565597"},
    {"Instituto de Seguridad Laboral": "2565760"},
    {"Servicio Nacional de Capacitación y Empleo": "2565805"},
    {"Superintendencia de Pensiones": "2565247"},
    {"Superintendencia de Seguridad Social": "2566003"},
]

for nombre in NOMBRES:
    institucion = Institucion.objects.get(nombre=list(nombre.keys())[0])
    codigo_pmg = nombre[list(nombre.keys())[0]]

    carga = institucion.cargas.filter(status='aprobado').order_by('-id').first()
    if carga is None:
        print("no hay carga para institucion {}".format(institucion.nombre))
        continue

    url = "https://8bl8xgahz9.execute-api.sa-east-1.amazonaws.com/prod/portal/carga/pdf_presentacion/{}/".format(carga.id)

    archivo = '{}_Certificado_Red_Satisfaccion_2021.pdf'.format(codigo_pmg)
    r = requests.get(url, stream=True)
    with open('../certificados/{}'.format(archivo), 'wb') as fd:
        for chunk in r.iter_content(80000):
            f = fd.write(chunk)

    url = carga.data["url"]
    url = url.replace('None', 'satisfaccion2021-web-archivos')
    url = url.replace('s3-satisfaccion2021-web', 'satisfaccion2021-web')
    url = url.replace('amazonaws.com/satisfaccion2021-web-archivos', '')
    url = url.replace('archivos.', 'archivos.s3.sa-east-1.amazonaws.com')

    archivo = '{}_Informe_Medicion_2021.{}'.format(codigo_pmg, url.split(".")[-1])
    r = requests.get(url, stream=True)
    with open('../informes/{}'.format(archivo), 'wb') as fd:
        for chunk in r.iter_content(80000):
            f = fd.write(chunk)
