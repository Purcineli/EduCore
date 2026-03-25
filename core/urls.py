from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('institucional.urls')),
    path('', include('usuarios.urls')),
    path('academic/', include('academico.urls')),
    path('communication/', include('comunicacao.urls')),
]
