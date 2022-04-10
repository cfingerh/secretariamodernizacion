from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_swagger.views import get_swagger_view
from django.urls import include, path


schema_view = get_swagger_view(title='API')

urlpatterns = [
    # path('__debug__/', include('debug_toolbar.urls')),
    url(r'^api/', include('base.urls')),

    url(r'^doc/$', schema_view),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('admin/', admin.site.urls),
    path('portal/', include('portal.urls')),
    path('usuarios/', include('usuarios.urls')),

]
