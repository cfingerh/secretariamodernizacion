# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def crear_permisos_base(user, agencias):
    permiso_ver_agencia = { 'tipo': 'ver',
                        'sobre': 'agencia',
                        'id': []
                        }
    permiso_editar_agencia = { 'tipo': 'editar',
                        'sobre': 'agencia',
                        'id': []
                        }
    permiso_crear_agencia = { 'tipo': 'crear',
                        'sobre': 'agencia',
                        'id': []
                        }
    permiso_ver_subdireccion = { 'tipo': 'ver',
                        'sobre': 'subdireccion',
                        'id': []
                        }
    permiso_editar_subdireccion = { 'tipo': 'editar',
                        'sobre': 'subdireccion',
                        'id': []
                        }
    permiso_crear_subdireccion = { 'tipo': 'crear',
                        'sobre': 'subdireccion',
                        'id': []
                        }
    permiso_ver_instrumento = { 'tipo': 'ver',
                        'sobre': 'instrumento',
                        'id': []
                        }
    permiso_editar_instrumento = { 'tipo': 'editar',
                        'sobre': 'instrumento',
                        'id': []
                        }
    permiso_crear_instrumento = { 'tipo': 'crear',
                        'sobre': 'instrumento',
                        'id': []
                        }
    permisos = []
    for agencia in agencias:
        if user.tipo_usuario == 'Administrador':
            permiso_ver_agencia['id'].append(agencia.id)
            permiso_editar_agencia['id'].append(agencia.id)
            permiso_crear_agencia['id'].append(agencia.id)
        elif user.tipo_usuario == 'Revisor Ministerio' or \
            user.tipo_usuario == 'Encargado Agencia':
            permiso_ver_agencia['id'].append(agencia.id)
        for subdireccion in agencia.subdirecciones.all():
            if user.tipo_usuario == 'Administrador':
                permiso_ver_subdireccion['id'].append(subdireccion.id)
                permiso_editar_subdireccion['id'].append(subdireccion.id)
                permiso_crear_subdireccion['id'].append(subdireccion.id)
            elif user.tipo_usuario == 'Revisor Ministerio':
                permiso_ver_subdireccion['id'].append(subdireccion.id)
                permiso_editar_subdireccion['id'].append(subdireccion.id)
            elif user.tipo_usuario == 'Encargado Agencia' or \
                user.tipo_usuario == 'Encargado Subdirección':
                permiso_ver_subdireccion['id'].append(subdireccion.id)
            for instrumento in subdireccion.instrumentos.all():
                if user.tipo_usuario == 'Administrador':
                    permiso_ver_instrumento['id'].append(instrumento.id)
                    permiso_editar_instrumento['id'].append(instrumento.id)
                    permiso_crear_instrumento['id'].append(subdireccion.id)
                elif user.tipo_usuario == 'Revisor Ministerio':
                    permiso_ver_instrumento['id'].append(instrumento.id)
                    permiso_editar_instrumento['id'].append(instrumento.id)
                elif user.tipo_usuario == 'Encargado Agencia' or \
                    user.tipo_usuario == 'Encargado Subdirección':
                    permiso_ver_instrumento['id'].append(instrumento.id)
                    permiso_editar_instrumento['id'].append(instrumento.id)
    permisos.append(permiso_ver_instrumento)
    permisos.append(permiso_editar_instrumento)
    permisos.append(permiso_crear_instrumento)
    permisos.append(permiso_ver_subdireccion)
    permisos.append(permiso_editar_subdireccion)
    permisos.append(permiso_crear_subdireccion)
    permisos.append(permiso_ver_agencia)
    permisos.append(permiso_editar_agencia)
    permisos.append(permiso_crear_agencia)

    return permisos

def send_email_acceso(data):
    subject = 'Acceso Intranet Observatorio'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = data['email']
    template = 'usuarios/mail_contraseña.html'

    html_content = render_to_string(template, {'username': data['username'], 
                                    'password':data['password'],
                                    'nombre_completo' : data['nombre_completo'],
                                    'url': data['url']}) 
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()