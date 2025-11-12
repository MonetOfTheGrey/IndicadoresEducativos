"""
───────────────────────────────────────────── ⋆⋅ ♰ ⋅⋆ ─────────────────────────────────────────────────
                        Proyecciones poblacionales a mitad de año 1950-2070
                                        Fuente: CONAPO
┏━━━━━━━━━━━━━━━━ ★ ━━━━━━━━━━━━━━━━━━━━┓
Nombre del archivo: limpiar_proyecciones_poblacionales.py

Autor: Javier Delgado Vargas

Fecha de creación:      23 - Junio - 2025
Última modificación:    25 - Junio - 2025

Descripción:
            Este archivo accede a la base de datos,
            particularmente el modelo "ProyeccionesPoblacionales"
            para modificar el archivo de nombre "00_Pob_Mitad_1950_2070.csv".
            La modificacion consiste en seleccionar solo los datos
            de la entidad federativa de Zacatecas y colocarlos
            en una nuevo archivo CSV de nombre "32_Pob_Mitad_1950_2070.csv".

->Creado tomando como referencia scripts para el proyecto "Estadística 911"

Recomendación músical del día:

        N-Wise Allah - Too Much Basura
https://youtu.be/SYvNV2gFVRo?si=ygKvBWIgLloX7sK9

        "Aposté todo a esto.
        No tengo plan B"
┗━━━━━━━━━━━━━━━━ ★ ━━━━━━━━━━━━━━━━━━━━┛
───────────────────────────────────────────── ⋆⋅ ♰ ⋅⋆ ─────────────────────────────────────────────────
"""
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.storage import default_storage
from panel_datos.models import ProyeccionesPoblacionales
import pandas as pd
from datetime import date
# Para almacenar el archivo final
import io
import os
import re

class LimpiadorDeProyeccionesPoblacionales:
    # Constructor de la clase
    def __init__(self):
        # Base de datos
        self.proyeccion_poblacional = None
        # Modelo de la base de datos
        self.modelo_de_proyecciones = ProyeccionesPoblacionales.objects.all()
        # Archivo final
        self.Poblacion_Mitad_2000_2070 = None

    def extraer_proyecciones(self):
        """
        ╔══════════•⊱✦⊰•══════════╗
               PROYECCIONES 
               POBLACIONALES
        ╚══════════•⊱✦⊰•══════════╝
        """
        print("\033[34mExtrayendo proyeccion poblacional.\033[0m")
        try:
            indice_archivo = 0
            # Se obtiene el objeto mediante el modelo
            self.proyeccion_poblacional = self.modelo_de_proyecciones[indice_archivo]
            # Se extrae la ruta del archivo
            self.proyeccion_poblacional = self.proyeccion_poblacional.archivo.path
            # comprobando que exista
            if default_storage.exists(self.proyeccion_poblacional):
                self.proyeccion_poblacional = pd.read_csv(
                    self.proyeccion_poblacional,
                    sep=',', low_memory=False
                )
                print("\033[32mSe leyó con éxito el archivo de proyecciones poblacionales\033[0m")
            
        except Exception as e:
             print(f'\033[31mError en la lectura del archivo de proyecciones poblacionaeles\n{e}\033[0m')

    def cargar_data_frame(self):
        print("\033[34mCargando datos en memoria'\033[0m")
        # Se carga el dataframe en memoria
        self.data_frame_proyeccion = self.proyeccion_poblacional.copy()        

    def eliminar_columnas(self):
        print("\033[34mEliminando columnas'\033[0m")
        # Se elimina la columna de renglon, de todas maneras la cantidad de registros se modificará
        self.data_frame_proyeccion = self.data_frame_proyeccion.drop('RENGLON', axis=1)
        # Se elimina la columna del identificador "32"
        self.data_frame_proyeccion = self.data_frame_proyeccion.drop('CVE_GEO', axis=1)

    def eliminar_filas(self):
        print("\033[34mEliminando filas'\033[0m")
        cantidad_de_registros_pre_entidad = len(self.data_frame_proyeccion.index)
        # Se eliminan las filas que no sean "Zacatecas"
        self.data_frame_proyeccion = self.data_frame_proyeccion[self.data_frame_proyeccion['ENTIDAD'] == 'Zacatecas']
        cantidad_de_registros_post_entidad = len(self.data_frame_proyeccion.index)
        # Eliminando filas de antes del año 2000
        self.data_frame_proyeccion = self.data_frame_proyeccion[self.data_frame_proyeccion['AÑO'].astype(int) > 2000]
        self.data_frame_proyeccion = self.data_frame_proyeccion[self.data_frame_proyeccion['AÑO'].astype(int) < 2030]
        self.data_frame_proyeccion = self.data_frame_proyeccion[self.data_frame_proyeccion['EDAD'].astype(int) >= 3]
        self.data_frame_proyeccion = self.data_frame_proyeccion[self.data_frame_proyeccion['EDAD'].astype(int) <= 30]
        cantidad_de_registros_post_año = len(self.data_frame_proyeccion.index)
        print("\033[32mDatos de la limpieza")
        print('Antes de eliminar registros por entidad:' f'{cantidad_de_registros_pre_entidad:,}')
        print('Después de eliminar registros por entidad:' f'{cantidad_de_registros_post_entidad:,}')
        print('Después de eliminar registros por año:' f'{cantidad_de_registros_post_año:,}''\033[0m')

    def generar_archivo_final(self, user):
        print("\033[34mGenerando y almacenando archivo final\033[0m")
        buffer = io.StringIO()
        self.data_frame_proyeccion.to_csv(buffer, index=False)
        
        # Se obtiene el contenido como string
        contenido_csv = buffer.getvalue().encode('utf-8')
        archivo = ContentFile(contenido_csv)

        # Buscar si ya existe una proyección con ese nombre
        nombre_archivo = 'zacatecas_proyecciones_poblacion_2000_2070'
        instancia_existente = ProyeccionesPoblacionales.objects.filter(nombre=nombre_archivo).first()

        if instancia_existente:
            # Encuentra una que ya existe
            print("\033[33mYa existe una instancia. Será actualizada.\033[0m")
            instancia_existente.actualizado_por = user
            instancia_existente.fecha_actualizacion = date.today()
            instancia_existente.archivo.save(f'{nombre_archivo}.csv', archivo, save=False)
            instancia_existente.save()
            try:
                # Funcion para evitar duplicidades en la base de datos
                funcion_actualizar_archivo()
                print("\033[32mSe ha actualizado el archivo correctamente\033[0m")
            except Exception as e:
                print(f"\n\nError al ejecutar actualizar archivo auxiliar: {e}\n\n")
        else:
            print("\033[32mCreando nueva instancia.\033[0m")
            nueva_instancia = ProyeccionesPoblacionales(
                actualizado_por=user,
                nombre=nombre_archivo,
                fecha_actualizacion=date.today()
            )
            nueva_instancia.archivo.save(f'{nombre_archivo}.csv', archivo)

def funcion_actualizar_archivo():
    print("\033[33mActualizando instancia existente\033[0m")
    # Se mueve de directorio
    os.chdir("/app/Sis_Ind_Edu/media/csv_pob_mitad")
    # Se listan los archivos en el directorio 
    print("\033[33mListando archivos en el directorio\033[0m")
    archivos = os.listdir(os.getcwd())

    # Declaración de variables de control
    contador_coincidencias = 0
    nombre_archivo_nuevo = ''

    print("\033[33m---> Actualizando zacatecas_proyecciones_poblacion_2000_2070 <---\033[0m")
    # Se itera sobre la lista de archivos
    for archivo in archivos:
        # Se busca un archivo de nombre exacto
        if re.search(r"zacatecas_proyecciones_poblacion_2000_2070\.csv$", archivo):
            contador_coincidencias += 1
            print("\033[33m\t1->Archivo antiguo encontrado.\033[0m")

        # Se busca un archivo nuevo con sufijo aleatorio
        if re.search(r"zacatecas_proyecciones_poblacion_2000_2070.+\.csv$", archivo):
            contador_coincidencias += 1
            print("\033[33m\t2->Archivo nuevo encontrado.\033[0m")
            nombre_archivo_nuevo = archivo

    # Si se detectaron ambos archivos, se actualiza
    if contador_coincidencias >= 2:
        os.remove("zacatecas_proyecciones_poblacion_2000_2070.csv")
        print("\033[33m\t3->Archivo antiguo eliminado.\033[0m")
        os.rename(nombre_archivo_nuevo, "zacatecas_proyecciones_poblacion_2000_2070.csv")
        print("\033[33m\t4->Archivo nuevo renombrado.\033[0m")

        # Actualizar el campo 'archivo' del modelo
        try:
            ProyeccionesPoblacionales.objects.filter(
                nombre="zacatecas_proyecciones_poblacion_2000_2070"
            ).update(archivo="csv_pob_mitad/zacatecas_proyecciones_poblacion_2000_2070.csv")
        except Exception as e:
            print(f"\033[31m\tError al actualizar el campo 'archivo': {e}\033[0m")

def principal(user):
    print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━ ★ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\nInicia Modulo para limpiar proyecciones poblacionales\n")
    # Se inicializa la clase
    limpiador_de_datos = LimpiadorDeProyeccionesPoblacionales()
    # Se obtiene la base de datos
    limpiador_de_datos.extraer_proyecciones()
    # Se carga el dataframe
    limpiador_de_datos.cargar_data_frame()
    # Se eliminan columnas
    limpiador_de_datos.eliminar_columnas()
    # Se eliminan filas y columnas innecesarias
    limpiador_de_datos.eliminar_filas()
    # Se almacena mediante el modelo de datos
    limpiador_de_datos.generar_archivo_final(user)
    print("\nTermina Modulo para limpiar proyecciones poblacionales\n┗━━━━━━━━━━━━━━━━━━━━━━━━ ★ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")