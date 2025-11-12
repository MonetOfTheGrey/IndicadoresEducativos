"""
URL configuration for IndicadoresEdu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from usuarios import views as vistas_usuarios
from panel_datos import views as vistas_panel_datos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vistas_usuarios.blank, name='blank'),
    path('iniciar_sesion', vistas_usuarios.iniciar_sesion, name='iniciar_sesion'),
    path('panel_datos', vistas_panel_datos.panel_datos, name='panel_datos'),
    path('agregar911', vistas_panel_datos.agregar_911, name='agregar911'),
    path('agregar_definicion', vistas_panel_datos.agregar_definicion, name='agregar_definicion'),
    path('subir_definicion', vistas_panel_datos.subir_definicion, name='subir_definicion'),
    path('agregar_algoritmo', vistas_panel_datos.agregar_algoritmo, name='agregar_algoritmo'),
    path('subir_algoritmo', vistas_panel_datos.subir_algoritmo, name='subir_algoritmo'),
    path('agregar_interpretacion', vistas_panel_datos.agregar_interpretacion, name='agregar_interpretacion'),
    path('subir_interpretacion', vistas_panel_datos.subir_interpretacion, name='subir_interpretacion'),
    path('subir_archivos_911', vistas_panel_datos.subir_archivos_911, name='subir_archivos_911'),
    path('agregar_conapo', vistas_panel_datos.agregar_conapo, name='agregar_conapo'),
    path('subir_archivos_conapo', vistas_panel_datos.subir_archivos_conapo, name='subir_archivos_conapo'),
    path('limpiar_proyecciones_poblacionales', vistas_panel_datos.limpiar_proyecciones_poblacionales, name='limpiar_proyecciones_poblacionales'),
    path('actualizar_cobertura_escolar', vistas_panel_datos.actualizar_cobertura_escolar, name='actualizar_cobertura_escolar'),    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
