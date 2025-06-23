from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Modelo de los ciclos escolares
class CiclosEscolares(models.Model):
    # Este campo solo perimte valores desde 2000 hasta 2100
    inicio = models.PositiveIntegerField(primary_key=True,
        validators=[MinValueValidator(2000),
                    MaxValueValidator(2100)])

    fin = models.PositiveIntegerField(
        validators=[MinValueValidator(2000),
                    MaxValueValidator(2100)])

'''
╔─━━━━━━━ ★ ━━━━━━━─╗
Modelo de Educación
Inicial
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class EducacionInicial(models.Model):
    id = models.AutoField(primary_key=True)
    # Se liga directamente al objeto del usuario
    # En vistas o plantillas se puede mostrar el primer nombre mediante: archivo.usuario.first_name
    actualizado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    ciclo_escolar_inicio = models.ForeignKey(
        CiclosEscolares,
        related_name='inicio_edu_inicial',
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=100)
    fecha_actualizacion = models.DateField("Fecha de actualizacion")
    archivo = models.FileField(upload_to='txt_inicial/')
'''
╔─━━━━━━━ ★ ━━━━━━━─╗
Modelo de Educación
Preescolar
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class EducacionPreescolar(models.Model):
    id = models.AutoField(primary_key=True)
    actualizado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    ciclo_escolar_inicio = models.ForeignKey(
        CiclosEscolares,
        related_name='inicio_edu_preescolar',
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=100)
    fecha_actualizacion = models.DateField("Fecha de actualizacion")
    archivo = models.FileField(upload_to='txt_preescolar/')
'''
╔─━━━━━━━ ★ ━━━━━━━─╗
Modelo de Educación
Primaria
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class EducacionPrimaria(models.Model):
    id = models.AutoField(primary_key=True)
    actualizado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    ciclo_escolar_inicio = models.ForeignKey(
        CiclosEscolares,
        related_name='inicio_edu_primaria',
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=100)
    fecha_actualizacion = models.DateField("Fecha de actualizacion")
    archivo = models.FileField(upload_to='txt_primaria/')
'''
╔─━━━━━━━ ★ ━━━━━━━─╗
Modelo de Educación
Secundaria
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class EducacionSecundaria(models.Model):
    id = models.AutoField(primary_key=True)
    actualizado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    ciclo_escolar_inicio = models.ForeignKey(
        CiclosEscolares,
        related_name='inicio_edu_secundaria',
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=100)
    fecha_actualizacion = models.DateField("Fecha de actualizacion")
    archivo = models.FileField(upload_to='txt_secundaria/')
'''
╔─━━━━━━━ ★ ━━━━━━━─╗
Modelo de Educación
Media Superior
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class EducacionMediaSuperior(models.Model):
    id = models.AutoField(primary_key=True)
    actualizado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    ciclo_escolar_inicio = models.ForeignKey(
        CiclosEscolares,
        related_name='inicio_edu_med_sup',
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=100)
    fecha_actualizacion = models.DateField("Fecha de actualizacion")
    archivo = models.FileField(upload_to='txt_media_superior/')
'''
╔─━━━━━━━ ★ ━━━━━━━─╗
Modelo de Educación
Media Superior
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class EducacionSuperior(models.Model):
    id = models.AutoField(primary_key=True)
    actualizado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    ciclo_escolar_inicio = models.ForeignKey(
        CiclosEscolares,
        related_name='inicio_edu_superior',
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=100)
    fecha_actualizacion = models.DateField("Fecha de actualizacion")
    archivo = models.FileField(upload_to='txt_superior/')