from django.contrib.auth.models import AbstractUser
try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField
from django.db import models


class User(AbstractUser):
    """
        Extend del modelo de usuario. 

    """
    permisos = JSONField(null=True, blank=True)

    @property
    def get_nombre_completo(self):
        return '%s %s' % (self.first_name, self.last_name)
