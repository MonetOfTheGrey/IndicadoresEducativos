from django.core.files.storage import default_storage
from panel_datos.models import EducacionPreescolar, EducacionInicial, MarginacionLocalidad
import pandas as pd
import numpy as np

class CoberturaEscolarPreescolar:
    def __init__(self):
        # Modelos utilizados
        self.modelo_preescolar = EducacionPreescolar.objects.all()
        self.modelo_inicial = EducacionInicial.objects.all()
        # Data frames utilizadods
        self.data_frame_preescolar = None
        self.data_frame_preescolar_rural = None
        self.data_frame_inicial = None
        self.data_frame_inicial_rural = None
        self.data_frame_final = None
        self.data_frame_marginacion_localidad = None
        # Lista de datos extraidos
        self.cobertura_preescolar_lista = []

    def obtener_911_preescolar(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
            EDUCACIÓN PREESCOLAR
        ╚══════════•⊱✦⊰•══════════╝
        """
        print(f"\033[34mObteniendo base de datos 911 de Educación Preescolar {ciclo_escolar}.\033[0m")
        for base_preescolar in self.modelo_preescolar:
            # Se corrobora que sea del ciclo especificado y que no sea Comunitaria Rural
            if (base_preescolar.ciclo_escolar_inicio == ciclo_escolar) and ("Comunitaria Rural" not in base_preescolar.nombre):
                # Se extrae la ruta del archivo
                archivo = base_preescolar.archivo
                print(f"\033[32mBase 911 de Educación Preescolar {ciclo_escolar} obtenidas con éxito:\n{archivo}\033[0m")
                # Se asigna el objeto completo
                ed_preescolar = base_preescolar
                # Se obtiene la ruta real del archivo
                direccion_ed_preescolar = ed_preescolar.archivo.path
                # Se corrobora que la ruta exista
                if default_storage.exists(direccion_ed_preescolar):
                    # Si existe entonces se intenta leer
                    try:
                        self.data_frame_preescolar = pd.read_csv(
                            direccion_ed_preescolar,
                            sep = '|', low_memory = False
                        )
                        print(f"\033[32mBase 911 de Educación Preescolar {ciclo_escolar} leída con éxito:\n{archivo}\033[0m")
                        #print(f"\033[32m{self.data_frame_preescolar.head(5)}\033[0m")
                    except Exception as e:
                        print(f'\033[31mError leyendo base 911 Educación Preescolar {ciclo_escolar}:\n{e}\033[0m')
                else:
                    print(f'\033[31mEl archivo no existe en la ruta: {direccion_ed_preescolar}\033[0m')

    def obtener_911_preescolar_comunitaria(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
            EDUCACIÓN PREESCOLAR
            COMUNITARIA RURAL
        ╚══════════•⊱✦⊰•══════════╝
        """
        print(f"\033[34mObteniendo base de datos 911 de Educación Preescolar Comunitaria Rural {ciclo_escolar}.\033[0m")
        for base_preescolar in self.modelo_preescolar:
            if (base_preescolar.ciclo_escolar_inicio == ciclo_escolar) and ("Comunitaria Rural" in base_preescolar.nombre):
                    # Se extrae la ruta del archivo
                    archivo = base_preescolar.archivo
                    print(f"\033[32mBase 911 de Educación Preescolar Comunitaria Rural {ciclo_escolar} obtenidas con éxito:\n{archivo}\033[0m")
                    # Se asigna el objeto completo
                    ed_preescolar_rural = base_preescolar
                    # Se obtiene la ruta real del archivo
                    direccion_ed_preescolar_rural = ed_preescolar_rural.archivo.path
                    # Se corrobora que la ruta exista
                    if default_storage.exists(direccion_ed_preescolar_rural):
                        # Si existe entonces se intenta leer
                        try:
                            self.data_frame_preescolar_rural = pd.read_csv(
                                direccion_ed_preescolar_rural,
                                sep = '|', low_memory = False
                            )
                            print(f"\033[32mBase 911 de Educación Preescolar Comunitaria Rural {ciclo_escolar} leída con éxito:\n{archivo}\033[0m")
                            #print(f"\033[32m{self.data_frame_preescolar_rural.head(5)}\033[0m")
                        except Exception as e:
                            print(f'\033[31mError leyendo base 911 Educación Preescolar Comunitaria Rural {ciclo_escolar}:\n{e}\033[0m')
                    else:
                        print(f'\033[31mEl archivo no existe en la ruta: {direccion_ed_preescolar_rural}\033[0m')

    def obtener_911_inicial(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
            EDUCACIÓN INICIAL
        ╚══════════•⊱✦⊰•══════════╝
        """
        print(f"\033[34mObteniendo base de datos 911 de Educación Inicial {ciclo_escolar}.\033[0m")
        for base_inicial in self.modelo_inicial:
            print(base_inicial.archivo)
            # Se corrobora que sea del ciclo especificado y que no sea Comunitaria Rural
            if (base_inicial.ciclo_escolar_inicio == ciclo_escolar) and ("Comunitaria Rural" not in base_inicial.nombre):
                # Se extrae la ruta del archivo
                archivo = base_inicial.archivo
                print(f"\033[32mBase 911 de Educación Inicial {ciclo_escolar} obtenidas con éxito:\n{archivo}\033[0m")
                # Se asigna el objeto completo
                ed_inicial = base_inicial
                # Se obtiene la ruta real del archivo
                direccion_ed_inicial = ed_inicial.archivo.path
                # Se corrobora que la ruta exista
                if default_storage.exists(direccion_ed_inicial):
                    # Si existe entonces se intenta leer
                    try:
                        self.data_frame_inicial = pd.read_csv(
                            direccion_ed_inicial,
                            sep = '|', low_memory = False
                        )
                        print(f"\033[32mBase 911 de Educación Inicial {ciclo_escolar} leída con éxito:\n{archivo}\033[0m")
                        #print(f"\033[32m{self.data_frame_inicial.head(5)}\033[0m")
                    except Exception as e:
                        print(f'\033[31mError leyendo base 911 Educación Inicial {ciclo_escolar}:\n{e}\033[0m')
                else:
                    print(f'\033[31mEl archivo no existe en la ruta: {direccion_ed_inicial}\033[0m')

    def obtener_911_inicial_comunitaria_rural(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
            EDUCACIÓN INICIAL
            COMUNITARIA RURAL
        ╚══════════•⊱✦⊰•══════════╝
        """
        # Solamente el ciclo escolar 2024-2025 contiene comunitaria Rural inicial
        if ciclo_escolar.inicio >= 2024:
            print(f"\033[34mObteniendo base de datos 911 de Educación Inicial Comunitaria Rural {ciclo_escolar}.\033[0m")
            for base_inicial in self.modelo_inicial:
                # Se corrobora que sea del ciclo especificado y que no sea Comunitaria Rural
                if (base_inicial.ciclo_escolar_inicio == ciclo_escolar) and ("Comunitaria Rural" in base_inicial.nombre):
                    # Se extrae la ruta del archivo
                    archivo = base_inicial.archivo
                    print(f"\033[32mBase 911 de Educación Inicial Comunitaria Rural {ciclo_escolar} obtenidas con éxito:\n{archivo}\033[0m")
                    # Se asigna el objeto completo
                    ed_inicial = base_inicial
                    # Se obtiene la ruta real del archivo
                    direccion_ed_inicial = ed_inicial.archivo.path
                    # Se corrobora que la ruta exista
                    if default_storage.exists(direccion_ed_inicial):
                        # Si existe entonces se intenta leer
                        try:
                            self.data_frame_inicial_rural = pd.read_csv(
                                direccion_ed_inicial,
                                sep = '|', low_memory = False
                            )
                            print(f"\033[32mBase 911 de Educación Inicial Comunitaria Rural {ciclo_escolar} leída con éxito:\n{archivo}\033[0m")
                            #print(f"\033[32m{self.data_frame_inicial_rural.head(5)}\033[0m")
                        except Exception as e:
                            print(f'\033[31mError leyendo base 911 Educación Inicial Comunitaria Rural {ciclo_escolar}:\n{e}\033[0m')
                    else:
                        print(f'\033[31mEl archivo no existe en la ruta: {direccion_ed_inicial}\033[0m')
        else:
            print(f'\033[31mCiclos escolares anteriores a 2024-2025 no cuentan com Educación Inicial Comunitaria Rural \033[0m')
   
    def obtener_marginacion_por_localidad(self):
        marginacion_localidad_xlsx = None
        marginacion_localidad_xlsx = MarginacionLocalidad.objects.order_by('fecha_actualizacion').first()
        # Comprobacion de que el modelo no está vacio
        if(marginacion_localidad_xlsx != None):
            marginacion_localidad_xlsx = marginacion_localidad_xlsx.archivo.path
            # Comprobacion de que existe en el almacenamiento (ruta)
            if(default_storage.exists(marginacion_localidad_xlsx)):
                try:
                    print(default_storage.path(marginacion_localidad_xlsx))
                    print("*--*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*-*-*-")
                    # Se intenta leer el archivo excel utilizando la ruta recortada
                    self.data_frame_marginacion_localidad = pd.read_excel(marginacion_localidad_xlsx, sheet_name='IML_2020_2')
                    print("Se leyó con exito el archivo de Marginación por Localidad")
                except Exception as e:
                    print(f"Error al leer el archivo: {e}")
            else:
                print(f"El archivo no existe en la ruta {marginacion_localidad_xlsx}")
        else:
            print("El modelo esta vacio")

    def limpiar_911_inicial(self):
        """
        ╔══════════•⊱✦⊰•══════════╗
                FILTRO DE
            EDUCACIÓN INICIAL
        ╚══════════•⊱✦⊰•══════════╝
        """
        print(f"\033[34mFiltrando registros de Educación Inicial\033[0m")
        try:
            self.data_frame_inicial = self.data_frame_inicial[
                self.data_frame_inicial['CV_CCT'].str.contains(r'NDI|SDI|DDI|EDI', na=False)
            ]
            self.data_frame_inicial = self.data_frame_inicial[self.data_frame_inicial['V175'] == 1]
            print("\n\t\033[32mFiltrado de Educación Inicial concluido.\033[0m")
        except Exception as e:
            print(f'\033[31mSe produjo un error en el filtrado de Educación Inicial:\n\t{e}\033[0m') 

    def extraer_estatus_captura(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
            ESTATUS DE CAPTURA
        ╚══════════•⊱✦⊰•══════════╝
        """
        print(f"\033[34mFiltrando registros por Estatus Captura\033[0m")
        try: 
            if self.data_frame_inicial is None:
                raise ValueError("self.data_frame_inicial es None")
            if self.data_frame_preescolar is None:
                raise ValueError("self.data_frame_preescolar es None")
            if self.data_frame_preescolar_rural is None:
                raise ValueError("self.data_frame_preescolar_rural es None")

            estatus_captura_inicial = pd.DataFrame({
                "CV_ESTATUS_CAPTURA": self.data_frame_inicial['CV_ESTATUS_CAPTURA']
            })
            estatus_captura = pd.DataFrame({
                "CV_ESTATUS_CAPTURA": self.data_frame_preescolar['CV_ESTATUS_CAPTURA']
            })
            estatus_captura_rural = pd.DataFrame({
                "CV_ESTATUS_CAPTURA": self.data_frame_preescolar_rural['CV_ESTATUS_CAPTURA']
            })

            # Se concatenan los dataframes
            if (ciclo_escolar.inicio >= 2024) and (self.data_frame_inicial_rural is not None):
                # De cumplirse ambos parametros, se extrae y se concatena junto con los demas dataframes
                # Extraccion primero
                estatus_caputra_inicial_rural = pd.DataFrame({
                    "CV_ESTATUS_CAPTURA": self.data_frame_inicial_rural['CV_ESTATUS_CAPTURA']
                })
                # Concatenación
                estatus_captura_concentrado = pd.concat(
                    [estatus_captura_inicial, estatus_caputra_inicial_rural, estatus_captura, estatus_captura_rural]
                )
            else:
                estatus_captura_concentrado = pd.concat(
                    [estatus_captura_inicial, estatus_captura, estatus_captura_rural],
                    ignore_index=True
                )

            # Se almacena en la lista
            self.cobertura_preescolar_lista.append(estatus_captura_concentrado)
            print("\n\t\033[32mExtracción de Estatus Captura concluido.\033[0m")
        except Exception as e:
            print(f'\033[31mSe produjo un error en la extracción del Estatus de Captura:\n\t{e}\033[0m')


    def extraer_cv_ct(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
                CLAVES DE
            CENTROS DE TRABAJO
        ╚══════════•⊱✦⊰•══════════╝
        """
        try:
            print(f"\033[34mExtrayendo Claves de Centro de Trabajo.\033[0m")
            CVCT_inicial = pd.DataFrame({
                'Clave de CT': self.data_frame_inicial['CV_CCT']
            })

            CVCT_preescolar = pd.DataFrame({
                'Clave de CT': self.data_frame_preescolar['CV_CCT']
            })
            CVCT_preescolar_comunitaria = pd.DataFrame({
                'Clave de CT': self.data_frame_preescolar_rural['CV_CCT']
            })
            if (ciclo_escolar.inicio >= 2024) and (self.data_frame_inicial_rural is not None):
                # De cumplirse ambos parametros, se extrae y se concatena junto con los demas dataframes
                # Para inicial comunitaria se contemplan "Menos de un año", "1 año" y "2 Años"
                CVCT_inicial_rural = pd.DataFrame({
                    'Clave de CT': self.data_frame_inicial_rural['CV_CCT']
                })
                # Concatenación
                CVCT_data_frame = pd.concat(
                    [CVCT_inicial, CVCT_inicial_rural,
                     CVCT_preescolar, CVCT_preescolar_comunitaria],
                    ignore_index = True
                )
            else:
                # Se concatenan
                CVCT_data_frame = pd.concat(
                    [CVCT_inicial,
                     CVCT_preescolar,
                     CVCT_preescolar_comunitaria],
                    ignore_index = True
                )
            self.cobertura_preescolar_lista.append(CVCT_data_frame)
            print('\n\t\033[32mExtraer Claves de Centro de Trabajo concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Claves de Centro de Trabajo:\n\t{e}\033[0m')

#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
#                          Menores de 3 años
#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.

    def extraer_matricula_menores_3_años_hombres(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
            MATRICULA MENORES
                3 AÑOS HOMBRES
        ╚══════════•⊱✦⊰•══════════╝
        """
        try:
            print(f"\033[34mExtrayendo Matricula menores de 3 años por sexo: hombres.\033[0m")
            alumnos_hombres_menores_3_años_inicial = pd.DataFrame({
                'Alumnos menores de 3 años hombres': self.data_frame_inicial['V461']
            })

            alumnos_hombres_menores_3_años_preescolar = pd.DataFrame({
                'Alumnos menores de 3 años hombres': self.data_frame_preescolar['V160']
            })
            alumnos_hombres_menores_3_años_preescolar_comunitaria = pd.DataFrame({
                'Alumnos menores de 3 años hombres': self.data_frame_preescolar_rural['V80']
            })
            if (ciclo_escolar.inicio >= 2024) and (self.data_frame_inicial_rural is not None):
                # De cumplirse ambos parametros, se extrae y se concatena junto con los demas dataframes
                # Para inicial comunitaria se contemplan "Menos de un año", "1 año" y "2 Años"
                # Se crea un dataframe extrayendo las 3 columnas necesarias
                inicial_rural_4_columnas = pd.DataFrame({
                    'Menos de un año': self.data_frame_inicial_rural['V64'],
                    '1 año': self.data_frame_inicial_rural['V67'],
                    '2 años': self.data_frame_inicial_rural['V70']
                })
                # Se crea una cuarta columna que sume los tres datos obtenidos en el paso anterior
                inicial_rural_4_columnas['Alumnos menores de 3 años'] = (
                    inicial_rural_4_columnas['Menos de un año'] +
                    inicial_rural_4_columnas['1 año'] +
                    inicial_rural_4_columnas['2 años']
                )
                alumnos_hombres_menores_3_años_inicial_rural = pd.DataFrame({
                    'Alumnos menores de 3 años hombres': inicial_rural_4_columnas['Alumnos menores de 3 años']
                })
                # Concatenación
                matricula_hombres_3_años = pd.concat(
                    [alumnos_hombres_menores_3_años_inicial, alumnos_hombres_menores_3_años_inicial_rural, 
                     alumnos_hombres_menores_3_años_preescolar, alumnos_hombres_menores_3_años_preescolar_comunitaria],
                    ignore_index = True
                )
            else:
                # Se concatenan
                matricula_hombres_3_años = pd.concat(
                    [alumnos_hombres_menores_3_años_inicial,
                     alumnos_hombres_menores_3_años_preescolar, 
                     alumnos_hombres_menores_3_años_preescolar_comunitaria],
                    ignore_index = True
                )
            self.cobertura_preescolar_lista.append(matricula_hombres_3_años)
            print('\n\t\033[32mExtraer Matricula menores de 3 años por sexo hombres concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Matricula menores de 3 años por sexo hombres:\n\t{e}\033[0m')

    def extraer_matricula_menores_3_años_mujeres(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
            MATRICULA MENORES
                3 AÑOS MUEJRES
        ╚══════════•⊱✦⊰•══════════╝
        """
        try:
            print(f"\033[34mExtrayendo Matricula menores de 3 años por sexo: mujeres.\033[0m")
            alumnos_mujeres_menores_3_años_inicial = pd.DataFrame({
                'Alumnos menores de 3 años mujeres': self.data_frame_inicial['V467']
            })

            alumnos_mujeres_menores_3_años_preescolar = pd.DataFrame({
                'Alumnos menores de 3 años mujeres': self.data_frame_preescolar['V166']
            })
            alumnos_mujeres_menores_3_años_preescolar_comunitaria = pd.DataFrame({
                'Alumnos menores de 3 años mujeres': self.data_frame_preescolar_rural['V86']
            })
            if (ciclo_escolar.inicio >= 2024) and (self.data_frame_inicial_rural is not None):
                # De cumplirse ambos parametros, se extrae y se concatena junto con los demas dataframes
                # Para inicial comunitaria se contemplan "Menos de un año", "1 año" y "2 Años"
                # Se crea un dataframe extrayendo las 3 columnas necesarias
                inicial_rural_4_columnas = pd.DataFrame({
                    'Menos de un año': self.data_frame_inicial_rural['V65'],
                    '1 año': self.data_frame_inicial_rural['V68'],
                    '2 años': self.data_frame_inicial_rural['V71']
                })
                # Se crea una cuarta columna que sume los tres datos obtenidos en el paso anterior
                inicial_rural_4_columnas['Alumnos menores de 3 años'] = (
                    inicial_rural_4_columnas['Menos de un año'] +
                    inicial_rural_4_columnas['1 año'] +
                    inicial_rural_4_columnas['2 años']
                )
                alumnos_mujeres_menores_3_años_inicial_rural = pd.DataFrame({
                    'Alumnos menores de 3 años mujeres': inicial_rural_4_columnas['Alumnos menores de 3 años']
                })
                # Concatenación
                matricula_mujeres_menores_3_años = pd.concat(
                    [alumnos_mujeres_menores_3_años_inicial, alumnos_mujeres_menores_3_años_inicial_rural,
                     alumnos_mujeres_menores_3_años_preescolar, alumnos_mujeres_menores_3_años_preescolar_comunitaria],
                    ignore_index = True
                )
            else:
                # Se concatenan
                matricula_mujeres_menores_3_años = pd.concat(
                    [alumnos_mujeres_menores_3_años_inicial,
                     alumnos_mujeres_menores_3_años_preescolar, 
                     alumnos_mujeres_menores_3_años_preescolar_comunitaria],
                    ignore_index = True
                )
            self.cobertura_preescolar_lista.append(matricula_mujeres_menores_3_años)
            print('\n\t\033[32mExtraer Matricula menores de 3 años por sexo mujeres concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Matricula 3 años por sexo mujeres:\n\t{e}\033[0m')

    def extraer_matricula_menores_3_años_total(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
            MATRICULA TOTAL
            MENORES 3 AÑOS
        ╚══════════•⊱✦⊰•══════════╝
        """
        try:
            print(f"\033[34mExtrayendo Matricula total menores de 3 años.\033[0m")
            alumnos_menores_3_años_inicial = pd.DataFrame({
                'Total alumnos menores de 3 años': self.data_frame_inicial['V473']
            })

            alumnos_menores_3_años_preescolar = pd.DataFrame({
                'Total alumnos menores de 3 años': self.data_frame_preescolar['V172']
            })
            alumnos_menores_3_años_preescolar_comunitaria = pd.DataFrame({
                'Total alumnos menores de 3 años': self.data_frame_preescolar_rural['V92']
            })
            if (ciclo_escolar.inicio >= 2024) and (self.data_frame_inicial_rural is not None):
                # De cumplirse ambos parametros, se extrae y se concatena junto con los demas dataframes
                # Para inicial comunitaria se contemplan "Menos de un año", "1 año" y "2 Años"
                # Se crea un dataframe extrayendo las 3 columnas necesarias
                inicial_rural_4_columnas = pd.DataFrame({
                    'Menos de un año': self.data_frame_inicial_rural['V66'],
                    '1 año': self.data_frame_inicial_rural['V69'],
                    '2 años': self.data_frame_inicial_rural['V72']
                })
                # Se crea una cuarta columna que sume los tres datos obtenidos en el paso anterior
                inicial_rural_4_columnas['Alumnos menores de 3 años'] = (
                    inicial_rural_4_columnas['Menos de un año'] +
                    inicial_rural_4_columnas['1 año'] +
                    inicial_rural_4_columnas['2 años']
                )
                alumnos_menores_3_años_inicial_rural = pd.DataFrame({
                    'Total alumnos menores de 3 años': inicial_rural_4_columnas['Alumnos menores de 3 años']
                })
                # Concatenación
                matricula_menores_3_años = pd.concat(
                    [alumnos_menores_3_años_inicial, alumnos_menores_3_años_inicial_rural, 
                     alumnos_menores_3_años_preescolar, alumnos_menores_3_años_preescolar_comunitaria],
                    ignore_index = True
                )
            else:
                # Se concatenan
                matricula_menores_3_años = pd.concat(
                    [alumnos_menores_3_años_inicial,
                     alumnos_menores_3_años_preescolar, 
                     alumnos_menores_3_años_preescolar_comunitaria],
                    ignore_index = True
                )
            self.cobertura_preescolar_lista.append(matricula_menores_3_años)
            print('\n\t\033[32mExtraer Matricula total menores de 3 años concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Matricula total menores de 3 años:\n\t{e}\033[0m')
#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
#                           Edad 3 años
#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.

    def extraer_matricula_3_años_hombres(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
                MATRICULA
                3 AÑOS HOMBRES
        ╚══════════•⊱✦⊰•══════════╝
        """
        try:
            print(f"\033[34mExtrayendo Matricula 3 años por sexo: hombres.\033[0m")
            alumnos_hombres_3_años_inicial = pd.DataFrame({
                'Alumnos de 3 años hombres': self.data_frame_inicial['V462']
            })

            alumnos_hombres_3_años_preescolar = pd.DataFrame({
                'Alumnos de 3 años hombres': self.data_frame_preescolar['V161']
            })
            alumnos_hombres_3_años_preescolar_comunitaria = pd.DataFrame({
                'Alumnos de 3 años hombres': self.data_frame_preescolar_rural['V81']
            })
            if (ciclo_escolar.inicio >= 2024) and (self.data_frame_inicial_rural is not None):
                # De cumplirse ambos parametros, se extrae y se concatena junto con los demas dataframes
                # Extraccion primero
                alumnos_hombres_3_años_inicial_rural = pd.DataFrame({
                    "Alumnos de 3 años hombres": self.data_frame_inicial_rural['V73']
                })
                # Concatenación
                matricula_hombres_3_años = pd.concat(
                    [alumnos_hombres_3_años_inicial, alumnos_hombres_3_años_inicial_rural, 
                     alumnos_hombres_3_años_preescolar, alumnos_hombres_3_años_preescolar_comunitaria],
                    ignore_index = True
                )
            else:
                # Se concatenan
                matricula_hombres_3_años = pd.concat(
                    [alumnos_hombres_3_años_inicial, alumnos_hombres_3_años_preescolar, alumnos_hombres_3_años_preescolar_comunitaria],
                    ignore_index = True
                )
            self.cobertura_preescolar_lista.append(matricula_hombres_3_años)
            print('\n\t\033[32mExtraer Matricula 3 años por sexo hombres concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Matricula 3 años por sexo hombres:\n\t{e}\033[0m')

    def extraer_matricula_3_años_mujeres(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
                MATRICULA
                3 AÑOS MUJERES
        ╚══════════•⊱✦⊰•══════════╝
        """
        try:
            print(f"\033[34mExtrayendo Matricula 3 años por sexo: mujeres.\033[0m")
            alumnos_mujeres_3_años_inicial = pd.DataFrame({
                'Alumnos de 3 años mujeres': self.data_frame_inicial['V468']
            })

            alumnos_mujeres_3_años_preescolar = pd.DataFrame({
                'Alumnos de 3 años mujeres': self.data_frame_preescolar['V167']
            })
            alumnos_mujeres_3_años_preescolar_comunitaria = pd.DataFrame({
                'Alumnos de 3 años mujeres': self.data_frame_preescolar_rural['V87']
            })
            if (ciclo_escolar.inicio >= 2024) and (self.data_frame_inicial_rural is not None):
                # De cumplirse ambos parametros, se extrae y se concatena junto con los demas dataframes
                # Extraccion primero
                alumnos_mujeres_3_años_inicial_rural = pd.DataFrame({
                    'Alumnos de 3 años mujeres': self.data_frame_inicial_rural['V74']
                })
                # Concatenación
                matricula_mujeres_3_años = pd.concat(
                    [alumnos_mujeres_3_años_inicial, alumnos_mujeres_3_años_inicial_rural, 
                     alumnos_mujeres_3_años_preescolar, alumnos_mujeres_3_años_preescolar_comunitaria],
                    ignore_index = True
                )
            else:
                # Se concatenan
                matricula_mujeres_3_años = pd.concat(
                    [alumnos_mujeres_3_años_inicial, alumnos_mujeres_3_años_preescolar, alumnos_mujeres_3_años_preescolar_comunitaria],
                    ignore_index = True
                )
            self.cobertura_preescolar_lista.append(matricula_mujeres_3_años)
            print('\n\t\033[32mExtraer Matricula 3 años por sexo mujeres concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Matricula 3 años por sexo mujeres:\n\t{e}\033[0m')

    def extraer_matricula_total_3_años(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
            MATRICULA TOTAL
                3 AÑOS
        ╚══════════•⊱✦⊰•══════════╝
        Revisando notas para el cálculo de indicadores educativos (previos al desarrollo de esta plataforma)
        En los cálculos de la cobertura específica de preescolar solo se contempla el rango de edades de:
        3, 4 y 5 años.
        No se contemplan menores de 3 años ni matricula de 6 años.
        """
        try:
            print(f"\033[34mExtrayendo Matricula Total 3 años.\033[0m")
            alumnos_3_años_inicial = pd.DataFrame({
                'Total alumnos de 3 años': self.data_frame_inicial['V474']
            })

            alumnos_3_años_preescolar = pd.DataFrame({
                'Total alumnos de 3 años': self.data_frame_preescolar['V173']
            })
            alumnos_3_años_preescolar_comunitaria = pd.DataFrame({
                'Total alumnos de 3 años': self.data_frame_preescolar_rural['V93']
            })
            if (ciclo_escolar.inicio >= 2024) and (self.data_frame_inicial_rural is not None):
                # De cumplirse ambos parametros, se extrae y se concatena junto con los demas dataframes
                # Extraccion primero
                alumnos_3_años_inicial_rural = pd.DataFrame({
                    'Total alumnos de 3 años': self.data_frame_inicial_rural['V75']
                })
                # Concatenación
                matricula_total_3_años = pd.concat(
                    [alumnos_3_años_inicial, alumnos_3_años_inicial_rural, 
                     alumnos_3_años_preescolar, alumnos_3_años_preescolar_comunitaria],
                    ignore_index = True
                )
            else:
                # Se concatenan
                matricula_total_3_años = pd.concat(
                    [alumnos_3_años_inicial, alumnos_3_años_preescolar, alumnos_3_años_preescolar_comunitaria],
                    ignore_index = True
                )
            self.cobertura_preescolar_lista.append(matricula_total_3_años)
            print('\n\t\033[32mExtraer Matricula 3 años por sexo mujeres concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Matricula Total 3 años:\n\t{e}\033[0m')

#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
#                           Edad 4 años
#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
    def extraer_matricula_4_años_hombres(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
                MATRICULA
                4 AÑOS HOMBRES
        ╚══════════•⊱✦⊰•══════════╝
        """
        try:
            print(f"\033[34mExtrayendo Matricula 4 años por sexo: hombres.\033[0m")
            alumnos_hombres_4_años_inicial = pd.DataFrame({
                'Alumnos de 4 años hombres': self.data_frame_inicial['V463']
            })

            alumnos_hombres_4_años_preescolar = pd.DataFrame({
                'Alumnos de 4 años hombres': self.data_frame_preescolar['V162']
            })
            alumnos_hombres_4_años_preescolar_comunitaria = pd.DataFrame({
                'Alumnos de 4 años hombres': self.data_frame_preescolar_rural['V82']
            })
            if (ciclo_escolar.inicio >= 2024) and (self.data_frame_inicial_rural is not None):
                # De cumplirse ambos parametros, se extrae y se concatena junto con los demas dataframes
                # Extraccion primero
                alumnos_hombres_4_años_inicial_rural = pd.DataFrame({
                    'Alumnos de 4 años hombres': self.data_frame_inicial_rural['V76']
                })
                # Concatenación
                matricula_hombres_4_años = pd.concat(
                    [alumnos_hombres_4_años_inicial, alumnos_hombres_4_años_inicial_rural, 
                     alumnos_hombres_4_años_preescolar, alumnos_hombres_4_años_preescolar_comunitaria],
                    ignore_index = True
                )
            else:
                # Se concatenan
                matricula_hombres_4_años = pd.concat(
                    [alumnos_hombres_4_años_inicial, alumnos_hombres_4_años_preescolar, alumnos_hombres_4_años_preescolar_comunitaria],
                    ignore_index = True
                )
            self.cobertura_preescolar_lista.append(matricula_hombres_4_años)
            print('\n\t\033[32mExtraer Matricula 4 años por sexo hombres concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Matricula 4 años por sexo hombres:\n\t{e}\033[0m')

    def extraer_matricula_4_años_mujeres(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
                MATRICULA
                4 AÑOS MUJERES
        ╚══════════•⊱✦⊰•══════════╝
        """
        try:
            print(f"\033[34mExtrayendo Matricula 4 años por sexo: mujeres.\033[0m")
            alumnos_mujeres_4_años_inicial = pd.DataFrame({
                'Alumnos de 4 años mujeres': self.data_frame_inicial['V469']
            })

            alumnos_mujeres_4_años_preescolar = pd.DataFrame({
                'Alumnos de 4 años mujeres': self.data_frame_preescolar['V168']
            })
            alumnos_mujeres_4_años_preescolar_comunitaria = pd.DataFrame({
                'Alumnos de 4 años mujeres': self.data_frame_preescolar_rural['V88']
            })
            if (ciclo_escolar.inicio >= 2024) and (self.data_frame_inicial_rural is not None):
                # De cumplirse ambos parametros, se extrae y se concatena junto con los demas dataframes
                # Extraccion primero
                alumnos_mujeres_4_años_inicial_rural = pd.DataFrame({
                    'Alumnos de 4 años mujeres': self.data_frame_inicial_rural['V77']
                })
                # Concatenación
                matricula_mujeres_4_años = pd.concat(
                    [alumnos_mujeres_4_años_inicial, alumnos_mujeres_4_años_inicial_rural, 
                     alumnos_mujeres_4_años_preescolar, alumnos_mujeres_4_años_preescolar_comunitaria],
                    ignore_index = True
                )
            else:
            # Se concatenan
                matricula_mujeres_4_años = pd.concat(
                    [alumnos_mujeres_4_años_inicial, alumnos_mujeres_4_años_preescolar, alumnos_mujeres_4_años_preescolar_comunitaria],
                    ignore_index = True
                )
            self.cobertura_preescolar_lista.append(matricula_mujeres_4_años)
            print('\n\t\033[32mExtraer Matricula 4 años por sexo mujeres concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Matricula 4 años por sexo mujeres:\n\t{e}\033[0m')

    def extraer_matricula_total_4_años(self, ciclo_escolar):
        """
        ╔══════════•⊱✦⊰•══════════╗
            MATRICULA TOTAL
                4 AÑOS
        ╚══════════•⊱✦⊰•══════════╝
        """
        try:
            print(f"\033[34mExtrayendo Matricula Total 4 años.\033[0m")
            alumnos_4_años_inicial = pd.DataFrame({
                'Total alumnos de 4 años': self.data_frame_inicial['V475']
            })

            alumnos_4_años_preescolar = pd.DataFrame({
                'Total alumnos de 4 años': self.data_frame_preescolar['V174']
            })
            alumnos_4_años_preescolar_comunitaria = pd.DataFrame({
                'Total alumnos de 4 años': self.data_frame_preescolar_rural['V94']
            })
            if (ciclo_escolar.inicio >= 2024) and (self.data_frame_inicial_rural is not None):
                # De cumplirse ambos parametros, se extrae y se concatena junto con los demas dataframes
                # Extraccion primero
                alumnos_4_años_inicial_rural = pd.DataFrame({
                    'Total alumnos de 4 años': self.data_frame_inicial_rural['V78']
                })
                # Concatenación
                matricula_total_4_años = pd.concat(
                    [alumnos_4_años_inicial, alumnos_4_años_inicial_rural, 
                     alumnos_4_años_preescolar, alumnos_4_años_preescolar_comunitaria],
                    ignore_index = True
                )
            else:
            # Se concatenan
                matricula_total_4_años = pd.concat(
                    [alumnos_4_años_inicial, alumnos_4_años_preescolar, alumnos_4_años_preescolar_comunitaria],
                    ignore_index = True
                )
            self.cobertura_preescolar_lista.append(matricula_total_4_años)
            print('\n\t\033[32mExtraer Matricula Total 4 años concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Matricula Total 4 años:\n\t{e}\033[0m')

#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
#                           Edad 5 años Inicial Comunitaria Rural no contempla edades despues de 4 años
#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
    def extraer_matricula_5_años_hombres(self):
        """
        ╔══════════•⊱✦⊰•══════════╗
                MATRICULA
                5 AÑOS HOMBRES
        ╚══════════•⊱✦⊰•══════════╝
        """
        try:
            print(f"\033[34mExtrayendo Matricula 5 años por sexo: hombres.\033[0m")
            alumnos_hombres_5_años_inicial = pd.DataFrame({
                'Alumnos de 5 años hombres': self.data_frame_inicial['V464']
            })

            alumnos_hombres_5_años_preescolar = pd.DataFrame({
                'Alumnos de 5 años hombres': self.data_frame_preescolar['V163']
            })
            alumnos_hombres_5_años_preescolar_comunitaria = pd.DataFrame({
                'Alumnos de 5 años hombres': self.data_frame_preescolar_rural['V83']
            })
            # Se concatenan
            matricula_hombres_5_años = pd.concat(
                [alumnos_hombres_5_años_inicial, alumnos_hombres_5_años_preescolar, alumnos_hombres_5_años_preescolar_comunitaria],
                ignore_index = True
            )
            self.cobertura_preescolar_lista.append(matricula_hombres_5_años)
            print('\n\t\033[32mExtraer Matricula 5 años por sexo hombres concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Matricula 5 años por sexo homrbes:\n\t{e}\033[0m')

    def extraer_matricula_5_años_mujeres(self):
        """
        ╔══════════•⊱✦⊰•══════════╗
                MATRICULA
                5 AÑOS MUJERES
        ╚══════════•⊱✦⊰•══════════╝
        """
        try:
            print(f"\033[34mExtrayendo Matricula 5 años por sexo: mujeres.\033[0m")
            alumnos_mujeres_5_años_inicial = pd.DataFrame({
                'Alumnos de 5 años mujeres': self.data_frame_inicial['V470']
            })

            alumnos_mujeres_5_años_preescolar = pd.DataFrame({
                'Alumnos de 5 años mujeres': self.data_frame_preescolar['V169']
            })
            alumnos_mujeres_5_años_preescolar_comunitaria = pd.DataFrame({
                'Alumnos de 5 años mujeres': self.data_frame_preescolar_rural['V89']
            })
            # Se concatenan
            matricula_mujeres_5_años = pd.concat(
                [alumnos_mujeres_5_años_inicial, alumnos_mujeres_5_años_preescolar, alumnos_mujeres_5_años_preescolar_comunitaria],
                ignore_index = True
            )
            self.cobertura_preescolar_lista.append(matricula_mujeres_5_años)
            print('\n\t\033[32mExtraer Matricula 5 años por sexo mujeres concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Matricula 5 años por sexo mujeres:\n\t{e}\033[0m')

    def extraer_matricula_total_5_años(self):
        """
        ╔══════════•⊱✦⊰•══════════╗
            MATRICULA TOTAL
                5 AÑOS
        ╚══════════•⊱✦⊰•══════════╝
        """
        try:
            print(f"\033[34mExtrayendo Matricula Total 5 años.\033[0m")
            alumnos_5_años_inicial = pd.DataFrame({
                'Total alumnos de 5 años': self.data_frame_inicial['V476']
            })

            alumnos_5_años_preescolar = pd.DataFrame({
                'Total alumnos de 5 años': self.data_frame_preescolar['V175']
            })
            alumnos_5_años_preescolar_comunitaria = pd.DataFrame({
                'Total alumnos de 5 años': self.data_frame_preescolar_rural['V95']
            })
            # Se concatenan
            matricula_total_5_años = pd.concat(
                [alumnos_5_años_inicial, alumnos_5_años_preescolar, alumnos_5_años_preescolar_comunitaria],
                ignore_index = True
            )
            self.cobertura_preescolar_lista.append(matricula_total_5_años)
            print('\n\t\033[32mExtraer Matricula Total 5 años concluido.\033[0m')
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo Matricula Total 5 años:\n\t{e}\033[0m')

#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
#                           Tratamiento final
#.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.

    def extraer_grado_de_marg(self):
        """
        ╔══════════•⊱✦⊰•══════════╗
            GRADO DE MARGINACION
        ╚══════════•⊱✦⊰•══════════╝
        NOTA IMPORTANTE: Este metodo es extenso y al terminar su ejecucion puede haber errores
                            en el grado de marginacion asignado a cada localidad.
                            Dichos errores se solucionan con los metodos al final de la clase
                            dedicados especificamente a limpiar los datos y corregir este 
                            tipo de detalles.
        """
        try:
            # Primero se debe construir un identificador total: estado, municipio, localidad.
            # Se crea un dataframe con el numero de municipio y localidad.
            
            id_inicial = pd.DataFrame({
                "Numero de municipio": self.data_frame_inicial['CV_MUN'].astype(str).str.zfill(3).tolist(),
                "Numero de localidad": self.data_frame_inicial['CV_LOC'].astype(str).str.zfill(4).tolist()
            })
            id_preescolar = pd.DataFrame({
                "Numero de municipio": self.data_frame_preescolar['CV_MUN'].astype(str).str.zfill(3).tolist(),
                "Numero de localidad": self.data_frame_preescolar['CV_LOC'].astype(str).str.zfill(4).tolist()
            })
            id_comunitaria_preescolar = pd.DataFrame({
                "Numero de municipio": self.data_frame_preescolar['CV_MUN'].astype(str).str.zfill(3).tolist(),
                "Numero de localidad": self.data_frame_preescolar['CV_LOC'].astype(str).str.zfill(4).tolist()
            })
            # Se concatenan
            gm_preescolar = pd.concat(
                [id_inicial, id_preescolar, id_comunitaria_preescolar],
                ignore_index = True
            )

            # Posterior a eso se inserta una columna al inicio del dataframe con valores "32", el dato faltante
            gm_preescolar.insert(0, "Codigo Estado", "32")
            # Se concatenan las tres columnas en ambos dataframes para crear 'CVE_LOC'
            gm_preescolar['CVE_LOC'] = (
                gm_preescolar['Codigo Estado'] + gm_preescolar['Numero de municipio'] + gm_preescolar['Numero de localidad']
            )
    
            # Se eliminan las columnas sobrantes
            gm_preescolar = gm_preescolar.drop('Codigo Estado', axis=1)
            gm_preescolar = gm_preescolar.drop('Numero de municipio', axis=1)
            gm_preescolar = gm_preescolar.drop('Numero de localidad', axis=1)
            """
            Ahora que el identificador esta construido se crea un diccionario
            con 'GM_LOC' y 'CVE_LOC'. Aunque primero hay que verificar que exisstan
            en el excel de marginacion por localidad
            """
            if ('GM_2020' not in self.data_frame_marginacion_localidad.columns or
                'CVE_LOC' not in self.data_frame_marginacion_localidad.columns):
                print("Una o ambas columnas 'GM_2020' o 'CVE_LOC' no se encontraron" +
                        "Verifique los nombres de las columnas en el archivo Excel.")
                return
            # Si el paso anterior fue exitoso se crea el diccionario de localidades y sus grados de marginacion
            diccionario_marginacion = self.data_frame_marginacion_localidad.set_index('CVE_LOC')['GM_2020'].to_dict()
            # Se verifica que ambas columnas 'CVE_LOC' tengan el formato correcto
            gm_preescolar['CVE_LOC'] = gm_preescolar['CVE_LOC'].str.strip() # Para eliminar espacios en blacnco
            self.data_frame_marginacion_localidad['CVE_LOC'] = self.data_frame_marginacion_localidad['CVE_LOC'].astype(str).str.strip()
            # Se usa el diccionario para mapear y crear la nuvea columna en 'gm_preescolar'
            diccionario_marginacion = self.data_frame_marginacion_localidad.set_index('CVE_LOC')['GM_2020'].to_dict()
            # Se mapean los valores de 'GM_2020' utilizando el diccionario
            gm_preescolar['Grado de marginacion'] = gm_preescolar['CVE_LOC'].map(diccionario_marginacion)
            # Se reemplazan los valores nulos por 'NO DISPONIBLE'
            gm_preescolar['Grado de marginacion'] = gm_preescolar['Grado de marginacion'].replace(np.nan, 'NO DISPONIBLE')
            """
            # Estas lineas son para imprimir los resultados de estos dataframes
            # Descomentar para hacer revisiones.
            print("Contenido de gm_preescolar después del mapeo:")
            print(gm_preescolar.head())
            print(gm_preescolar)
            """
            # Se elimina la columna del nombre de la localidad para evitar duplicados
            gm_preescolar = gm_preescolar.drop('CVE_LOC', axis=1)
            # Se reemplazan los valores nulos
            gm_preescolar = gm_preescolar.replace(np.nan, 'NO DISPONIBLE')
            # Se agrega el dataframe a la lista correspondiente
            self.cobertura_preescolar_lista.append(gm_preescolar)
            print("\n\tExtraer grado de marginacion concluido")
        except Exception as e:
            print(f'Hubo un error extrayendo el grado de marginacion:\n\t{e}')

    def crear_data_frame_final(self):
        try:
            print(f"\033[34mGenerando DataFrame Final\033[0m")
            # Se reinicia el indice de todos los dataframes para evitar que tenga errores al concatenar
            self.data_frame_final = pd.concat(
                [df.reset_index(drop=True) for df in self.cobertura_preescolar_lista],
                axis=1
            )
            #print(self.data_frame_final.head(5))
            #print(self.data_frame_final.tail(5))
            #print(self.data_frame_final.shape)
        except Exception as e:
            print(f'\033[31mHubo un error Generando el DataFrame Final:\n\t{e}\033[0m')

    def eliminar_estatus_captura(self):

        """
        ╔══════════•⊱✦⊰•══════════╗
        ELIMINAR ESTATUS CAPTURA
        ╚══════════•⊱✦⊰•══════════╝
        """
        # Lista de números enteros que señalan escuelas inactivas
        try:
            valores_a_eliminar = [1, 3, 4, 7]
            valores_a_conservar = [0, 10]
            # Para eliminar 1 3 4 y 7
            #self.data_frame_final = self.data_frame_final[~self.data_frame_final['CV_ESTATUS_CAPTURA'].isin(valores_a_eliminar)]
            # Para conservar 0 y 10 solamente
            self.data_frame_final = self.data_frame_final[self.data_frame_final['CV_ESTATUS_CAPTURA'].isin(valores_a_conservar)]
            self.data_frame_final.drop(columns=['CV_ESTATUS_CAPTURA'], inplace=True)
            print("\n\tEliminar estatus captura concluido")
            """
            # Descomentar para hacer analisis individual de los registros
            with pd.option_context('display.max_rows', None):
                print(self.data_frame_final[["Clave de CT", "Total alumnos menores de 3 años"]].to_string(index=False))

            #print(self.data_frame_final.head(5))
            #print(self.data_frame_final.shape)
            """
        except Exception as e:
            print(f'\033[31mHubo un error Eliminando estatus captura:\n\t{e}\033[0m')

    def devolver_data_frame_final(self):
        try:
            return self.data_frame_final
        except Exception as e:
            print(f'\033[31mHubo un error Dwevolviendo el dataframe final:\n\t{e}\033[0m')

def principal(ciclo_escolar_solicitado):
    # TODO: Quizas sea necesario incluir la SIC para hacer el manejo de marginacion por localidad
    # TODO: Atencion a 3 años, atencion a 4 años, atencion a 5 años, atencion a 3 4 y 5 años
    extractor_preescolar = CoberturaEscolarPreescolar()
    extractor_preescolar.obtener_911_preescolar(ciclo_escolar_solicitado)
    extractor_preescolar.obtener_911_preescolar_comunitaria(ciclo_escolar_solicitado)
    extractor_preescolar.obtener_911_inicial(ciclo_escolar_solicitado)
    extractor_preescolar.obtener_911_inicial_comunitaria_rural(ciclo_escolar_solicitado)
    extractor_preescolar.obtener_marginacion_por_localidad()
    extractor_preescolar.limpiar_911_inicial()
    extractor_preescolar.extraer_estatus_captura(ciclo_escolar_solicitado)
    extractor_preescolar.extraer_cv_ct(ciclo_escolar_solicitado)
    extractor_preescolar.extraer_matricula_menores_3_años_hombres(ciclo_escolar_solicitado)
    extractor_preescolar.extraer_matricula_menores_3_años_mujeres(ciclo_escolar_solicitado)
    extractor_preescolar.extraer_matricula_menores_3_años_total(ciclo_escolar_solicitado)
    extractor_preescolar.extraer_matricula_3_años_hombres(ciclo_escolar_solicitado)
    extractor_preescolar.extraer_matricula_3_años_mujeres(ciclo_escolar_solicitado)
    extractor_preescolar.extraer_matricula_total_3_años(ciclo_escolar_solicitado)
    extractor_preescolar.extraer_matricula_4_años_hombres(ciclo_escolar_solicitado)
    extractor_preescolar.extraer_matricula_4_años_mujeres(ciclo_escolar_solicitado)
    extractor_preescolar.extraer_matricula_total_4_años(ciclo_escolar_solicitado)
    extractor_preescolar.extraer_matricula_5_años_hombres()
    extractor_preescolar.extraer_matricula_5_años_mujeres()
    extractor_preescolar.extraer_matricula_total_5_años()
    extractor_preescolar.extraer_grado_de_marg()
    # Tratamiento final
    extractor_preescolar.crear_data_frame_final()
    extractor_preescolar.eliminar_estatus_captura()
    dataframe_final = extractor_preescolar.devolver_data_frame_final()
    return(dataframe_final)
