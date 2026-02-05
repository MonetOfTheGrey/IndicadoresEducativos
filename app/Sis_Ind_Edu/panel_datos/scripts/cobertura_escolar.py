"""
───────────────────────────────────────────── ⋆⋅ ♰ ⋅⋆ ─────────────────────────────────────────────────
                                    Tasa Bruta de Escolarización
                                            A.K.A.
                                        Cobertura Escolar
┏━━━━━━━━━━━━━━━━ ★ ━━━━━━━━━━━━━━━━━━━━┓
Nombre del archivo: cobertura_escolar.py

Autor: Javier Delgado Vargas

Fecha de creación:      26 - Junio - 2025
Última modificación:    26 - Junio - 2025

Descripción:
            Este archivo accede a la base de datos
            para extraer las proyecciones poblacionales
            de Zacatecas. Mediante las cuales se calcula
            el indicador educativo de Cobertura Escolar
            en base al algoritmo dado por la SEP en
            Lineamientos para la Formulación de Indicadores
            Educativos.

Recomendación músical del día:

        Gaceloide - Barrotes
https://youtu.be/HtaroPXutcU?si=yXR53oyXgcjzvTZS

        "Pies de plomo,
        100 metros lisos,
        quedo en primero"
┗━━━━━━━━━━━━━━━━ ★ ━━━━━━━━━━━━━━━━━━━━┛
───────────────────────────────────────────── ⋆⋅ ♰ ⋅⋆ ─────────────────────────────────────────────────
"""
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
# Se necesitan todas las bases de datos, al menos por ahora
from panel_datos.models import *
import pandas as pd

class IndicadorCoberturaEscolar:
    # Constructor de la clase
    def __init__(self):
        # Base de datos
        self.proyeccion_poblacional = None
        # Modelos de la base de datos
        self.modelo_de_proyecciones = ProyeccionesPoblacionales.objects.all()
        self.modelo_cobertura_escolar = CoberturaEscolar.objects.all()
        self.modelo_ciclos_escolares = CiclosEscolares.objects.all()
        self.modelo_preescolar = EducacionPreescolar.objects.all()
        # Resultados del cálculo
        self.cobertura_total = None
        self.cobertura_preescolar = None
        self.cobertura_primaria = None
        self.cobertura_secundaria = None
        self.cobertura_media_superior = None
        self.cobertura_superior = None
        # Identificador de ciclos escolares existentes en el modelo
        self.ciclos_escolares = []
        self.ciclos_escolares_list = {}
        # Ciclos escolares de las coberturas no calculadas
        self.coberturas_no_calculadas = None
        # Ciclos escolares de atencion a 3, 4 y 5 años no calculadas
        self.atencion_no_calculadas = None
        # Ciclos escolares de bases de datos 911 existentes en los registros
        self.ciclos_escolares_911_existentes = []
        # Ciclos escolares de bases de datos 911 faltantes
        self.ciclos_escolares_911_faltantes =[]

    def obtener_ciclos_escolares(self):
        """
        ╔══════════•⊱✦⊰•══════════╗
               CICLOS ESCOLARES
        ╚══════════•⊱✦⊰•══════════╝
        """
        print("\033[34mObteniendo ciclos escolares\033[0m")
        for ciclo in self.modelo_ciclos_escolares:
            self.ciclos_escolares.append(ciclo.inicio)
        self.ciclos_escolares_list = list(CiclosEscolares.objects.values('inicio'))
        print("\033[32mCiclos escolares obtenidos con éxito\033[0m")

    def obtener_proyeccion_poblacional(self):
        """
        ╔══════════•⊱✦⊰•══════════╗
                PROYECCION 
                POBLACIONAL
        ╚══════════•⊱✦⊰•══════════╝
        """
        print("\033[34mExtrayendo proyeccion poblacional.\033[0m")
        try:
            indice_archivo = 1
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

    def excluding_join_coberturas_escolares(self):
        """
        ╔══════════•⊱✦⊰•══════════╗
                COBERTURAS 
                ESCOLARES
        ╚══════════•⊱✦⊰•══════════╝
        Este método toma dos modelos:
        Izquierdo - Ciclos escolares
        Derecho - Coberturas escolares
        La idea es hacer un left excluding join donde:
        Se obtengan los ciclos escolares que no existen en la tabla de coberturas escolares
        Esto con la finalidad de no calcular todos la cobertura escolar de todos los ciclos escolares siempre
        """
        print("\033[34mObteniendo ciclos escolares de coberturas no claculadas\033[0m")
        try:
            # Se obtienen los ciclos escolares con cobertura ya calculada
            ciclos_escolares_ya_calculados = CoberturaEscolar.objects.values_list('ciclo_escolar_inicio', flat=True)
            # Se filtran los objetos en CiclosEscolares que NO están en CoberturaEscolar
            ciclos_escolares_no_calculados = CiclosEscolares.objects.exclude(inicio__in=ciclos_escolares_ya_calculados)
            # Se almacenan en memoria
            self.coberturas_no_calculadas = ciclos_escolares_no_calculados.values_list('inicio', flat=True)
            print("\033[32mCiclos escolares de coberturas no calculadas obtenidas con éxito\033[0m")
        except Exception as e:
            print(f'\033[31mError en "excluding_join_coberturas_escolares"\n{e}\033[0m')


    def excluding_join_bases_911(self, modelo, nombre_modelo, campo_ciclo='ciclo_escolar_inicio'):
        """
        ╔══════════•⊱✦⊰•══════════╗
                BASES 911
        ╚══════════•⊱✦⊰•══════════╝
        Este método toma dos modelos:
        Izquierdo - Ciclos escolares
        Derecho - Bases 911
        La idea es hacer un left excluding join donde:
        Se obtengan los ciclos escolares que no existen en la tabla de bases 911
        Esto con la finalidad de evitar errores al calcular cobertura de ciclos que no tienen bases 911
        """
        try:
            ciclos_sin_base = []
            bases = list(modelo.objects.values('nombre', campo_ciclo))
            ciclos_con_base = [base[campo_ciclo] for base in bases]

            for ciclo in self.ciclos_escolares_list:

                # Se tiene que corregir desde aqui para que el sistema envie a calcular los ciclos anteriores a 2024 aunque estén incompletos en las bases de datos de inicial
                # La confirmación de que no se necesita inicial comunitaria rural
                if (ciclo['inicio'] < 2024) and (nombre_modelo == 'Educación Inicial'):
                    for base in bases:
                        # Si NO está cominitaria rural y es de un ciclo anterior a 2024
                        if (base['nombre'] != 'Inicial Comunitaria Rural') and (base['ciclo_escolar_inicio'] == ciclo['inicio']):
                            # No hace nada, no se agrega a los ciclos sin bases para que se puedan calcular
                            print(f"------>Se agregó una base INICIAL sin INICIAL COMUNITARIA RURAL {base['ciclo_escolar_inicio']}<------")

                elif (ciclo['inicio'] not in ciclos_con_base):
                    ciclos_sin_base.append(ciclo['inicio'])
                    print(f"\033[33mEl ciclo escolar {ciclo['inicio']} no cuenta con todas las bases de {nombre_modelo}\033[0m")
            return ciclos_sin_base
        except Exception as e:
            print(f'\033[31mError en "excluding_join_bases_911"\n{e}\033[0m')

    def excluding_join_atencion_poblacion_345(self):
        """
        ╔══════════•⊱✦⊰•══════════╗
                COBERTURAS
                ESCOLARES
        ╚══════════•⊱✦⊰•══════════╝
        Este método toma dos modelos:
        Izquierdo - Ciclos escolares
        Derecho - Atencion a la poblacion de 3, 4 y 5 años
        La idea es hacer un left excluding join donde:
        Se obtengan los ciclos escolares que no existen en la tabla de atención
        Esto con la finalidad de no calcular la atencion de todos los ciclos escolares siempre
        """
        print("\033[34mObteniendo ciclos escolares de atenciones no claculadas\033[0m")
        try:
            # Se obtienen los ciclos escolares con cobertura ya calculada
            ciclos_escolares_ya_calculados = AtencionPoblacion345.objects.values_list('ciclo_escolar_inicio', flat=True)
            # Se filtran los objetos en CiclosEscolares que NO están en AtencionPoblacion345
            ciclos_escolares_no_calculados = CiclosEscolares.objects.exclude(
                inicio__in=ciclos_escolares_ya_calculados
            )
            # Se almacenan en memoria
            self.atencion_no_calculadas = ciclos_escolares_no_calculados.values_list('inicio', flat=True)
            print("\033[32mCiclos escolares de atención a la poblacion de 3, 4 y 5 no calculadas obtenidas con éxito\033[0m")
        except Exception as e:
            print(f'\033[31mError en "excluding_join_atencion_poblacion_345"\n{e}\033[0m')
    
    def calcular_cobertura_escolar(self, ce_sin_inicial, ce_sin_preescolar, ce_sin_primaria,
                                   ce_sin_secundaria, ce_sin_med_sup, ce_sin_superior):
        # Se recorre cada ciclo en base de datos
        for ciclo in self.modelo_ciclos_escolares:
            # Se corrobora que no esté en la lista de bases 911 incompletas
            if ((ciclo.inicio not in ce_sin_inicial) and (ciclo.inicio not in ce_sin_preescolar)
                and (ciclo.inicio not in ce_sin_primaria) and (ciclo.inicio not in ce_sin_secundaria)
                and (ciclo.inicio not in ce_sin_med_sup) and (ciclo.inicio not in ce_sin_superior)
                # Esta ultima linea corrobora que no se haya calculado ya la cobertura para ese ciclo
                and (ciclo.inicio in self.coberturas_no_calculadas) and (ciclo.inicio in self.coberturas_no_calculadas)
                ):
                # Si no está, se calcula la cobertura de todos los niveles para ese ciclo
                print(f'\033[32mSe calcula la cobertura para el ciclo escolar {ciclo.inicio}\033[0m')
                # Se manda a llamar al archivo que extrae las bases necesarias para preescolar
                from panel_datos.scripts import datos_para_cobertura_preescolar
                # Se ejecuta la funcion principal
                # Esto obtiene un dataframe
                datos_preescolar = datos_para_cobertura_preescolar.principal(ciclo)
                from panel_datos.scripts import atencion_edades_345
                atencion_edades_345.principal(ciclo, datos_preescolar, self.proyeccion_poblacional)
                # TODO: crear script para calcular la cobertura
        atencion_edades_345.graficos_multiples_ciclos(ciclo, datos_preescolar, self.proyeccion_poblacional)
        atencion_edades_345.graficos_multiples_ciclos(ciclo, datos_preescolar, self.proyeccion_poblacional)

def principal():
    print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━ ★ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("Inicia Modulo para calcular Cobertura Escolar\n")
    # Se inicializa la clase
    calculador_cobertura_escolar = IndicadorCoberturaEscolar()
    # Se obtienen los ciclos escoalres
    calculador_cobertura_escolar.obtener_ciclos_escolares()
    # Se obtiene la proyeccion poblacional de Zacatecas
    calculador_cobertura_escolar.obtener_proyeccion_poblacional()
    # Se hace el left excluding join para saber que Coberturas escolares no se han calculado aún
    calculador_cobertura_escolar.excluding_join_coberturas_escolares()
    # Se hace el left excluding join para saber que ciclos escolares no tienen 911
    print("\033[34mObteniendo ciclos escolares sin bases 911\033[0m")
    ciclos_escolares_sin_inicial = calculador_cobertura_escolar.excluding_join_bases_911(EducacionInicial, 'Educación Inicial')
    ciclos_escolares_sin_preescolar = calculador_cobertura_escolar.excluding_join_bases_911(EducacionPreescolar, 'Educación Preescolar')
    ciclos_escolares_sin_primaria = calculador_cobertura_escolar.excluding_join_bases_911(EducacionPrimaria, 'Educación Primaria')
    ciclos_escolares_sin_secundaria = calculador_cobertura_escolar.excluding_join_bases_911(EducacionSecundaria, 'Educación Secundaria')
    ciclos_escolares_sin_med_sup = calculador_cobertura_escolar.excluding_join_bases_911(EducacionMediaSuperior, 'Educación Media Superior')
    ciclos_escolares_sin_superior = calculador_cobertura_escolar.excluding_join_bases_911(EducacionSuperior, 'Educación Superior')
    # Se hace left excluding join para saber que ciclos escolares no tienen atencion a 3,4 y 5 años
    calculador_cobertura_escolar.excluding_join_atencion_poblacion_345()
    calculador_cobertura_escolar.calcular_cobertura_escolar(ciclos_escolares_sin_inicial, ciclos_escolares_sin_preescolar,
                                                            ciclos_escolares_sin_primaria, ciclos_escolares_sin_secundaria,
                                                            ciclos_escolares_sin_med_sup, ciclos_escolares_sin_superior)
    print("\nTermina Modulo para calcular Cobertura Escolar")
    # Necesita los datos de inicio de ciclo escolar 911
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━ ★ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")

# Educación Preescolar
# Educación Primaria
# Educación Secundaria
# Educación Media Superior
# Educación Superior
# Total