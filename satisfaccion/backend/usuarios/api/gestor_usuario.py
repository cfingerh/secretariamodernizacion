import secrets
import string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from base.models import Agencia, Subdireccion, Instrumento
# from base.pagination import AnalyzePagination
from usuarios.models import User
from usuarios.utils import crear_permisos_base, send_email_acceso

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                 'email',  'permisos', 'rut', 'cargo', 'numero_telefonico',
                 'get_nombre_completo', 'agencia', 'tipo_usuario')

    def validate_email(self, email):
        try:
            if self.instance:
                User.objects.exclude(pk=self.instance.pk).get(email=email)
            else:
                User.objects.get(email=email)
            raise serializers.ValidationError("Ya existe un usuario con ese correo registrado")
        except User.DoesNotExist:
            return email

class UserView(viewsets.ModelViewSet):
    """
        FRONTEND:\n
        views/CrearUsuario.vue views/ListarUsuarios.vue
    """
    queryset = User.objects.all().exclude(username='admin')
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    # pagination_class = AnalyzePagination
    filter_fields = ('id',)

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser or usuario.tipo_usuario == 'Administrador':
            return self.queryset
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        usuario = request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        if usuario.is_superuser or usuario.tipo_usuario == 'Administrador':
            self.perform_create(serializer)
        else:
            return Response('Usuario no autorizado', status=status.HTTP_401_UNAUTHORIZED, headers=None)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        user = serializer.save()
        if user.tipo_usuario == 'Administrador' or \
            user.tipo_usuario == 'Revisor Ministerio':
            agencias = Agencia.objects.all()
        else:
            agencias = Agencia.objects.filter(pk=user.agencia.id)
        if not user.permisos or len(user.permisos) == 0 or \
            agencia_anterior != user.agencia or \
            tipo_usuario_anterior != user.tipo_usuario:
            user.permisos = crear_permisos_base(user, agencias)
            user.save()
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        user.set_password(password)
        user.save()
        data = {'username': user.username,
                'email': user.email, 
                'nombre_completo': user.get_nombre_completo,
                'password': password,
                'url': 'https://dlm8lrmopk79r.cloudfront.net/' }
                
        send_email_acceso(data) 

    def update(self, request, *args, **kwargs):
        usuario = request.user
        if usuario.is_superuser or usuario.tipo_usuario == 'Administrador':
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def perform_update(self, serializer):
        anterior = self.get_object()
        agencia_anterior = anterior.agencia
        tipo_usuario_anterior = anterior.tipo_usuario
        user = serializer.save()
        if user.tipo_usuario == 'Administrador' or \
            user.tipo_usuario == 'Revisor Ministerio':
            agencias = Agencia.objects.all()
        else:
            agencias = Agencia.objects.filter(pk=user.agencia.id)
        if not user.permisos or len(user.permisos) == 0 or \
            agencia_anterior != user.agencia or \
            tipo_usuario_anterior != user.tipo_usuario:
            user.permisos = crear_permisos_base(user, agencias)
            user.save()

    def destroy(self, request, *args, **kwargs):
        usuario = request.user
        instance = self.get_object()
        if usuario.is_superuser or usuario.tipo_usuario == 'Administrador':
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)