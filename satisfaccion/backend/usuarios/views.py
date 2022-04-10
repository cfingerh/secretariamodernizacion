import json
from datetime import datetime

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from usuarios.models import User
import requests
import json
from urllib.parse import urlencode
import os
from rest_framework_simplejwt.tokens import RefreshToken


@csrf_exempt
def claveunica(request):

    if request.method != 'POST':
        return HttpResponse("No es POST")

    state = json.loads(request.body).get("state")
    code = json.loads(request.body).get("code")
    url = "https://accounts.claveunica.gob.cl/openid/token/"
    data = {
        'client_id': os.environ.get('CU_CLIENT_ID'),
        'client_secret': os.environ.get('CU_CLIENT_SECRET'),
        'redirect_uri': os.environ.get('CU_CALLBACK'),
        'grant_type': 'authorization_code',
        'code': code,
        'state': state,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    print("---------------------")
    print(data)
    resp = requests.post(url, data=urlencode(data), headers=headers)
    print(resp.text)
    data = json.loads(resp.text)
    access_token = data.get("access_token")

    url = "https://accounts.claveunica.gob.cl/openid/userinfo/"
    response = requests.post(url, auth=BearerAuth(access_token))
    datos_usuario = json.loads(response.text)
    rut = datos_usuario.get("RolUnico").get("numero")
    dv = datos_usuario.get("RolUnico").get("DV")
    user = User.objects.get_or_create(username__iexact="{}-{}".format(rut, dv))[0]
    try:
        nombre = "{} {} {} {}".format(datos_usuario.get("name").get("nombres")[0],
                                      datos_usuario.get("name").get("nombres")[1],
                                      datos_usuario.get("name").get("apellidos")[0],
                                      datos_usuario.get("name").get("apellidos")[1])
        user.nombre_completo = nombre
        user.save()

    except:
        pass
    refresh = RefreshToken.for_user(user)

    try:
        user.first_login = user.first_login or datetime.now()
        user.last_login = datetime.now()
        user.save()
    except:
        pass

    print({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

    return JsonResponse({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


@csrf_exempt
def login_with_hash(request):

    username = request.GET.get("username")
    import hashlib
    string_key = "{}_satisfaccion_bgi".format(username)

    hash_code = int(hashlib.sha1(string_key.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
    if str(hash_code) != str(request.GET.get("hash")):
        return

    user = User.objects.filter(username__iexact=username).order_by('id').first()
    if user is None:
        return
    refresh = RefreshToken.for_user(user)

    try:
        user.first_login = user.first_login or datetime.now()
        user.last_login = datetime.now()
        user.save()
    except:
        pass

    return JsonResponse({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


def is_user(request):
    username = request.GET.get("username")
    if User.objects.filter(username__iexact=username).order_by('id').first():
        return JsonResponse({'is_user': True})
    return JsonResponse({'is_user': False})


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def get_user(request):
    user = None
    if request.user and request.user.username:
        user = request.user

    try:
        if JWTAuthentication().authenticate(request):
            user = JWTAuthentication().authenticate(request)[0]
    except InvalidToken:
        user = None
    except AuthenticationFailed:
        user = None

    return user


def has_permission_to_edit(perfil, user, service):
    return True
    # elif perfil in ['satisfaccion', 'satisfaccion_empresa']:
    #     if ServiceUser.objects.filter(user=user, service=service, tipo__in=['superadministrador', 'administrador', 'representante', 'encargado', 'jefe_servicio']).first() is None:
    #         return False
    # elif perfil in ['funcionario']:
    #     if ServiceUser.objects.filter(user=user, service=service, tipo__in=['superadministrador', 'encargado', 'jefe_servicio']).first() is None:
    #         return False
    # else:
    #     return False

    # return True


@csrf_exempt
def eliminar(request):
    user = get_user(request)
    if user is None:
        return JsonResponse({'code': 'token_not_valid'}, status=401)

    service = Service.objects.get(pk=json.loads(request.body).get("service"))
    username = json.loads(request.body).get("username")
    perfil_a_eliminar = json.loads(request.body).get("tipo")

    if username is None:
        return JsonResponse({'code': 'missing_data', 'message': 'Falta Username'}, status=400)

    if not has_permission_to_edit(perfil_a_eliminar, user, service):
        return JsonResponse({'code': 'no_permission', 'message': 'No tiene permisos para eliminar'}, status=400)

    user_a_eliminar = User.objects.get(username=username)
    ServiceUser.objects.filter(
        user=user_a_eliminar, service=service, tipo=perfil_a_eliminar).delete()

    return getPerfiles(request, service_id=service.id)


@csrf_exempt
def agregar(request):
    user = get_user(request)
    if user is None:
        return JsonResponse({'code': 'token_not_valid'}, status=401)

    service = Service.objects.get(pk=json.loads(request.body).get("service"))
    rut = json.loads(request.body).get("rut")
    perfil_a_crear = json.loads(request.body).get("perfil")

    if perfil_a_crear not in ["administrador", "representante", "jefe_servicio", "encargado", "funcionario", "satisfaccion", "satisfaccion_empresa"]:
        return JsonResponse({'code': 'missing_data', 'message': 'Falta seleccionar tipo de perfil'}, status=400)

    if rut is None:
        return JsonResponse({'code': 'missing_data', 'message': 'Falta RUT'}, status=400)

    if not has_permission_to_edit(perfil_a_crear, user, service):
        return JsonResponse({'code': 'no_permission', 'message': 'No tiene permisos para crear'}, status=400)

    user, created = User.objects.get_or_create(username=rut)
    if created:
        user.nombre_completo = json.loads(request.body).get("nombre_completo")
        user.email = json.loads(request.body).get("email")
    user.save()

    su = ServiceUser.objects.get_or_create(user=user, service=service)[0]
    su.tipo = perfil_a_crear
    su.save()

    return getPerfiles(request, service_id=service.id)


def getPerfiles(request, service_id=None):
    user = get_user(request)
    if user is None:
        return JsonResponse({'code': 'token_not_valid'}, status=401)

    service = Service.objects.get(pk=service_id)
    # Permisos
    su = ServiceUser.objects.filter(user=user, service=service).first()
    if su is None:
        return JsonResponse({'message': 'Solo un Encargado puede agregar otro encargado'}, status=400)

    service_users = list(ServiceUser.objects.filter(service=service).values(
        'id',
        'user__username',
        'user__nombre_completo',
        'user__email',
        'tipo',
        'permisos'))

    return JsonResponse(service_users, safe=False)


@csrf_exempt
def change_modulos(request, serviceuser_id=None):
    user = get_user(request)
    if user is None:
        return JsonResponse({'code': 'token_not_valid'}, status=401)

    serviceuser = ServiceUser.objects.get(pk=serviceuser_id)
    serviceuser.permisos["modulos"] = json.loads(request.body)
    serviceuser.save()

    return getPerfiles(request, service_id=serviceuser.service_id)


def info(request):
    user = None
    if request.user and request.user.username:
        user = request.user

    try:
        if JWTAuthentication().authenticate(request):
            user = JWTAuthentication().authenticate(request)[0]
    except InvalidToken:
        user = None
    except AuthenticationFailed:
        user = None

    if user is None:
        return JsonResponse({'code': 'token_not_valid'}, status=401)

    # if user.service_set.all().count() == 0:
    #     return HttpResponse('No esta asociado a servicio', status=401)

    user.permisos = user.permisos or {}
    # tipos = list(set([i.tipo for i in ServiceUser.objects.filter(user=user)]))

    data = {
        'username': user.username,
        # 'is_staff': user.is_staff,
        'id': user.id,
        'email': user.email,
        # 'tipos': tipos,
        'nombre_completo': user.permisos.get("nombre_completo")
        # 'service': user.service.name,
        # 'serviceId': user.service.id,
        # 'ministry': user.service.ministry.name,
        # 'ministryId': user.service.ministry.id,

    }
    return JsonResponse(data, safe=False)


@ csrf_exempt
def register(request):

    data = json.loads(request.body)
    username = data.get("username")
    if username is None:
        return JsonResponse({'message': 'username_missing'}, status=400)

    if User.objects.filter(username=username).first():
        return JsonResponse({'message': 'username_exists'}, status=400)

    email = data.get("email")
    if email is None:
        return JsonResponse({'message': 'email_missing'}, status=400)

    if User.objects.filter(email=email).first():
        return JsonResponse({'message': 'email_exists'}, status=400)

    password = data.get("password")
    if password is None:
        return JsonResponse({'message': 'password_missing'}, status=400)

    user = User()
    user.email = email
    user.username = username
    user.set_password(password)
    user.save()

    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })
