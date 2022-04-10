from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets
from usuarios.models import User

class UserSerializer(serializers.ModelSerializer):

    agencia__nombre = serializers.CharField(source='agencia.nombre', 
                                            read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                 'email',  'permisos', 'tipo_usuario', 'is_superuser', 
                 'get_nombre_completo', 'agencia__nombre')

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id',)

    def get_queryset(self):
        queryset = self.queryset.filter(pk=self.request.user.id)
        return queryset