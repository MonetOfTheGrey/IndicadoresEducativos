from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
'''
╔─━━━━━━━ ★ ━━━━━━━─╗
    Proyecciones
    Poblacionales
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class ProyeccionesPoblacionales(models.Model):
    id = models.AutoField(primary_key=True)
    actualizado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    fecha_actualizacion = models.DateField("Fecha de actualizacion")
    archivo = models.FileField(upload_to='csv_pob_mitad/')


'''
╔─━━━━━━━ ★ ━━━━━━━─╗
Ciclos Escolares
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class CiclosEscolares(models.Model):
    # Este campo solo perimte valores desde 2000 hasta 2100
    inicio = models.PositiveIntegerField(primary_key=True,
        validators=[MinValueValidator(2000),
                    MaxValueValidator(2100)])

    fin = models.PositiveIntegerField(
        validators=[MinValueValidator(2000),
                    MaxValueValidator(2100)])

    def __str__(self):
        return f"{self.inicio}" 

'''
╔─━━━━━━━ ★ ━━━━━━━─╗
    Marginación 
    por Localidad
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class MarginacionLocalidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fecha_actualizacion = models.DateField("Fecha de actualizacion")
    archivo = models.FileField(upload_to='marginacion_por_localidad/')
    actualizado_por = models.ForeignKey(User, on_delete=models.CASCADE)
'''
╔─━━━━━━━ ★ ━━━━━━━─╗
    Atención a la
    Población 
    de 3, 4 y 5
        años
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class AtencionPoblacion345(models.Model):
    id = models.AutoField(primary_key = True)
    ciclo_escolar_inicio = models.ForeignKey(
        CiclosEscolares,
        related_name='inicio_atencion_poblacion_345',
        on_delete = models.CASCADE
    )
    # -----> Porcentajes de atención <-----
    porcentaje_atencion_hombres = models.DecimalField(
        max_digits = 5, decimal_places = 2
        # Esto permite un numero hasta 999.99
    )
    porcentaje_atencion_mujeres = models.DecimalField(
        max_digits = 5, decimal_places = 2
    )
    porcentaje_atencion_total = models.DecimalField(
        max_digits = 5, decimal_places = 2
    )
    # -----> Datos de Matricula 911 <-----
    matricula_hombres = models.IntegerField()
    matricula_mujeres = models.IntegerField()
    matricula_total = models.IntegerField()
    # -----> Datos de proyecciones CONAPO <-----
    proyeccion_conapo_poblacion_hombres = models.IntegerField()
    proyeccion_conapo_poblacion_mujeres = models.IntegerField()
    proyeccion_conapo_poblacion_total = models.IntegerField()
    # Grupo de edades
    grupo_de_edad_choices = [
        ("3", "3 años"),
        ("4", "4 años"),
        ("5", "5 años"),
        ("3-5", "3, 4 y 5 años")
    ]
    grupo_de_edad = models.CharField(max_length=3, choices=grupo_de_edad_choices)
    grafico = models.ImageField(upload_to='atencion_poblacion_edades_3_4_5/')
    fecha_actualizacion = models.DateField("Fecha de actualizacion")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ciclo_escolar_inicio', 'grupo_de_edad'],
                name='unique_atencion_por_ciclo_y_edad'
            )
        ]

class MarginacionPoblacion345(models.Model):
    id = models.AutoField(primary_key = True)
    ciclo_escolar_inicio = models.ForeignKey(
        CiclosEscolares,
        related_name='inicio_marginacion_poblacion_345',
        on_delete = models.CASCADE
    )
    # Porcentajes de marginacion
    porcentaje_muy_bajo = models.DecimalField(
        max_digits = 5, decimal_places = 2
    )
    porcentaje_bajo = models.DecimalField(
        max_digits = 5, decimal_places = 2
    )
    porcentaje_medio = models.DecimalField(
        max_digits = 5, decimal_places = 2
    )
    porcentaje_alto = models.DecimalField(
        max_digits = 5, decimal_places = 2
    )
    porcentaje_muy_alto = models.DecimalField(
        max_digits = 5, decimal_places = 2
    )
    # Matricula 911
    matricula_total = models.IntegerField()
    # Poblacion conapo
    proyeccion_conapo_poblacion_total = models.IntegerField()
    # Grupo de edades
    grupo_de_edad_choices = [
        ("3", "3 años"),
        ("4", "4 años"),
        ("5", "5 años"),
        ("3-5", "3, 4 y 5 años")
    ]
    grupo_de_edad = models.CharField(max_length=3, choices=grupo_de_edad_choices)
    grafico = models.ImageField(upload_to='marginacion_poblacion_edades_3_4_5/')
    fecha_actualizacion = models.DateField("Fecha de actualizacion")


'''
╔─━━━━━━━ ★ ━━━━━━━─╗
Definiciones de
Indicadores
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class IndicadorDefinicion(models.Model):
    # TODO: Convertir UNIQUE el campo indicador para evitar repetidos
    id = models.AutoField(primary_key=True)
    indicador_choices = [
        ("AE3", "Atención Edad 3 años"),
        ("AE4", "Atención Edad 4 años"),
        ("AE5", "Atención Edad 5 años"),
    ]
    indicador = models.CharField(
        max_length = 3,
        choices = indicador_choices
    )
    definicion = models.TextField(max_length=1000)

'''
╔─━━━━━━━ ★ ━━━━━━━─╗
Interpretación de
Indicadores
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class interpretaciones_indicadores(models.Model):
    id = models.AutoField(primary_key=True)
    indicador_choices = [
        ("AE3", "Atención Edad 3 años"),
        ("AE4", "Atención Edad 4 años"),
        ("AE5", "Atención Edad 5 años"),
    ]
    indicador = models.CharField(
        max_length = 3,
        choices = indicador_choices
    )
    interpretacion = models.TextField(max_length=1000)
'''
╔─━━━━━━━ ★ ━━━━━━━─╗
    Algoritmos 
    de indicadores
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class algoritmos_indicadores(models.Model):
    id = models.AutoField(primary_key=True)
    indicador_choices = [
        ("AE3", "Atención Edad 3 años"),
        ("AE4", "Atención Edad 4 años"),
        ("AE5", "Atención Edad 5 años"),
    ]
    indicador = models.CharField(
        max_length = 3,
        choices = indicador_choices
    )
    algoritmo = models.ImageField(upload_to='algoritmos_indicadores/')

'''
╔─━━━━━━━ ★ ━━━━━━━─╗
Gráficos múltiples 
    ciclos escolares
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class graficos_multiples(models.Model):
    id = models.AutoField(primary_key=True)
    primer_ciclo_escolar = models.ForeignKey(
        CiclosEscolares,
        related_name='primer_ciclo_grafico_multiple',
        on_delete=models.CASCADE
    )
    ultimo_ciclo_escolar = models.ForeignKey(
        CiclosEscolares,
        related_name='ultimo_ciclo_grafico_multiple',
        on_delete=models.CASCADE
    )
    # Elecciones del indicador que representa
    indicador_choices = {
        "AE3": "Atención Edad 3 años",
        "AE4": "Atención Edad 4 años",
        "AE5": "Atención Edad 5 años"
    }
    indicador = models.CharField(
        max_length = 3,
        choices = indicador_choices
    )
    grafico = models.ImageField(upload_to='graficos_multiplesciclos/')
    fecha_actualizacion = models.DateField("Fecha de actualizacion")

'''
╔─━━━━━━━ ★ ━━━━━━━─╗
    Cobertura
    Escolar
╚─━━━━━━━ ★ ━━━━━━━─╝
'''
class CoberturaEscolar(models.Model):
    id = models.AutoField(primary_key=True)
    ciclo_escolar_inicio = models.ForeignKey(
        CiclosEscolares,
        related_name='inicio_cobertura_escolar',
        on_delete=models.CASCADE
    )
    # Elecciones del nivel para el que se calcula el indicador
    nivel_choices = {
        "PE": "Preescolar",
        "PR": "Primaria",
        "SE": "Secundaria",
        "MS": "Media Superior",
        "SU": "Superior",
        "TO": "Total"
    }
    nivel = models.CharField(
        max_length = 2,
        choices = nivel_choices
        # No se asigna un valor por default
        )
    fecha_actualizacion = models.DateField("Fecha de actualizacion")
    valor = models.IntegerField()
    interpretacion = models.TextField(max_length=1000)
    formula_de_calculo = models.FileField(upload_to='formulas_cobertura_escolar/')

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