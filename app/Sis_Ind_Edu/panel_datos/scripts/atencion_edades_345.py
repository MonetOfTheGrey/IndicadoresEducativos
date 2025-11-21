
from django.core.files.base import ContentFile
# Se necesitan todas las bases de datos, al menos por ahora
from panel_datos.models import AtencionPoblacion345, graficos_multiples, MarginacionPoblacion345
import io
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import date

class CalculadoraCoberturaPreescolar:
    def __init__(self, ciclo_escolar_solicitado, datos_preescolar, proyeccion_poblacional):
        # Modelos utilizados
        self.modelo_atencion_poblacion345 = AtencionPoblacion345.objects.all()
        # Data frames utilizadods
        self.data_frame_final = datos_preescolar
        self.ciclo_escolar = ciclo_escolar_solicitado
        self.proyeccion_poblacional = proyeccion_poblacional
        # Datos del modelo

        self.datos = {
            "3": {
                "matricula": {"hombres": None, "mujeres": None, "total": None},
                "atencion": {"hombres": None, "mujeres": None, "total": None},
                "poblacion": {"hombres": None, "mujeres": None, "total": None},
                "matricula_gm": {"muy bajo": None, "bajo": None, "medio": None, "alto": None, "muy alto": None, "total": None},
                "porcentaje_matricula_gm": {"muy bajo": None, "bajo": None, "medio": None, "alto": None, "muy alto": None, "total": None},
            },
            "4": {
                "matricula": {"hombres": None, "mujeres": None, "total": None},
                "atencion": {"hombres": None, "mujeres": None, "total": None},
                "poblacion": {"hombres": None, "mujeres": None, "total": None},
            },
            "5": {
                "matricula": {"hombres": None, "mujeres": None, "total": None},
                "atencion": {"hombres": None, "mujeres": None, "total": None},
                "poblacion": {"hombres": None, "mujeres": None, "total": None},
            },
        }

    """
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 3 años⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    """
    def extraer_datos_3_años(self):
        try:
            print(f"\033[34mExtrayendo datos para Atención total a la Población de 3 años para el ciclo escolar {self.ciclo_escolar.inicio}\033[0m")
            # Menores de 3 años
            data_frame_total_mujeres_matricula_menor_3_años = self.data_frame_final['Alumnos menores de 3 años mujeres']
            data_frame_total_hombres_matricula_menor_3_años = self.data_frame_final['Alumnos menores de 3 años hombres']
            total_matricula_mujeres_menor_3_años = data_frame_total_mujeres_matricula_menor_3_años.sum()
            total_matricula_hombres_menor_3_años = data_frame_total_hombres_matricula_menor_3_años.sum()
            # Matricula de 3 años
            data_frame_total_hombres_matricula_3_años = self.data_frame_final['Alumnos de 3 años hombres']
            data_frame_total_mujeres_matricula_3_años = self.data_frame_final['Alumnos de 3 años mujeres']
            total_matricula_hombres_3_años = data_frame_total_hombres_matricula_3_años.sum()
            total_matricula_mujeres_3_años = data_frame_total_mujeres_matricula_3_años.sum()

            # Matricula total por sexo
            self.datos["3"]["matricula"]["mujeres"] = (total_matricula_mujeres_menor_3_años + total_matricula_mujeres_3_años)
            self.datos["3"]["matricula"]["hombres"] = (total_matricula_hombres_menor_3_años + total_matricula_hombres_3_años)
            self.datos["3"]["matricula"]["total"] = (
                    self.datos["3"]["matricula"]["hombres"] + self.datos["3"]["matricula"]["mujeres"]
            )
            # Poblacion
            df_poblacion = self.proyeccion_poblacional
            df_poblacion = df_poblacion[df_poblacion['EDAD'].astype(int) == 3]
            df_poblacion = df_poblacion[df_poblacion['AÑO'].astype(int) == self.ciclo_escolar.inicio]

            self.datos["3"]["poblacion"]["hombres"] = df_poblacion[df_poblacion['SEXO'] == 'Hombres']['POBLACION'].sum()
            self.datos["3"]["poblacion"]["mujeres"] = df_poblacion[df_poblacion['SEXO'] == 'Mujeres']['POBLACION'].sum()
            self.datos["3"]["poblacion"]["total"] = df_poblacion['POBLACION'].sum()
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo datos para Atención total a la Población de 3 años para el ciclo escolar {self.ciclo_escolar.inicio}:\n\t{e}\033[0m')

    def calcular_atencion_3_años(self):
        try:
            print(f"\033[34mCalculando atención para población de 3 años para el ciclo escolar {self.ciclo_escolar.inicio}\033[0m")
            # Atencion a hombres = (matricula_hombres / poblacion_total) * 100
            self.datos["3"]['atencion']['hombres'] = (
                self.datos["3"]["matricula"]["hombres"] / self.datos["3"]["poblacion"]["total"] ) * 100
            # Atencion a mujeres = (matricula_mujeres / poblacion_total) * 100
            self.datos["3"]["atencion"]["mujeres"] = (
                self.datos["3"]["matricula"]["mujeres"] / self.datos["3"]["poblacion"]["total"] ) * 100
            # Atencion total = (matricula_total / poblacion_total) * 100
            self.datos["3"]["atencion"]["total"] = (
                self.datos["3"]["matricula"]["total"] / self.datos["3"]["poblacion"]["total"] ) * 100

            print(f'Atención mujeres 3 años: {self.datos["3"]["atencion"]["mujeres"]}')
            print(f'Atención hombres 3 años: {self.datos["3"]["atencion"]["hombres"]}')
            print(f'Atención total 3 años: {self.datos["3"]["atencion"]["total"]}')
        except Exception as e:
            print(f'\033[31mHubo un error Calculando Atención total a la Población de 3 años para el ciclo escolar {self.ciclo_escolar.inicio}:\n\t{e}\033[0m')

    def generar_grafico_atencion_individual_poblacion_3_años(self):
        try:
            print(f"\033[34mGenerando Gráfico Atención individual a la Población total de 3 años para el ciclo escolar {self.ciclo_escolar.inicio}\033[0m")
            # Valores ya calculados
            valores_mujeres = self.datos["3"]["atencion"]["mujeres"]
            valores_hombres = self.datos["3"]["atencion"]["hombres"]
            valores_sin_atencion = 100 - (valores_mujeres + valores_hombres)

            # Datos para gráfica apilada
            categorias = ['Atención']
            porcentajes_mujeres = [valores_mujeres]
            porcentajes_hombres = [valores_hombres]
            porcentajes_restante = [valores_sin_atencion]

            # Paleta de colores estilo "mako"
            colores = sns.color_palette("mako", n_colors=3)

            # Creación de gráfico
            fig, ax = plt.subplots(figsize=(6, 6))

            # Apilamiento
            ax.bar(categorias, porcentajes_mujeres, label='Mujeres', color=colores[0])
            ax.bar(categorias, porcentajes_hombres, bottom=porcentajes_mujeres, label='Hombres', color=colores[1])
            ax.bar(categorias, porcentajes_restante,
                   bottom=[porcentajes_mujeres[0] + porcentajes_hombres[0]],
                   label='Sin atención', color=colores[2])

            # Etiquetas
            total_altura = [porcentajes_mujeres[0], porcentajes_hombres[0], porcentajes_restante[0]]
            acumulado = 0
            for i, valor in enumerate(total_altura):
                ax.text(0, acumulado + valor / 2, f'{valor:.1f}%', ha='center', va='center', color='white', fontsize=10)
                acumulado += valor

            # Estética
            ax.set_ylim(0, 110)
            ax.set_ylabel('Porcentaje')
            ax.set_title(f'Atención a población de 3 años ({self.ciclo_escolar.inicio})', fontsize=14)
            ax.set_xticks([])
            ax.legend(loc='upper right')

            # Guardar gráfico
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)

            # Se guarda la instancia directamente en el modelo
            instancia, _ = AtencionPoblacion345.objects.update_or_create(
                ciclo_escolar_inicio=self.ciclo_escolar,
                porcentaje_atencion_hombres=self.datos["3"]["atencion"]["hombres"],
                porcentaje_atencion_mujeres=self.datos["3"]["atencion"]["mujeres"],
                porcentaje_atencion_total=self.datos["3"]["atencion"]["total"],
                matricula_hombres = self.datos["3"]["matricula"]["hombres"],
                matricula_mujeres = self.datos["3"]["matricula"]["mujeres"],
                matricula_total = self.datos["3"]["matricula"]["total"],
                proyeccion_conapo_poblacion_hombres=self.datos["3"]["poblacion"]["hombres"],
                proyeccion_conapo_poblacion_mujeres=self.datos["3"]["poblacion"]["mujeres"],
                proyeccion_conapo_poblacion_total=self.datos["3"]["poblacion"]["total"],
                grupo_de_edad="3",
                fecha_actualizacion=date.today()
            )
            nombre_del_grafico = f"atencion_poblacion_edad_3_{self.ciclo_escolar.inicio}_{self.ciclo_escolar.fin}.png"
            instancia.grafico.save(nombre_del_grafico, ContentFile(buffer.read()), save=True)
            plt.close(fig)
            buffer.close()
        except Exception as e:
            print(f'\033[31mHubo un error generando Gráfico Atención total a la Población de 3 años para el ciclo escolar {self.ciclo_escolar.inicio}:\n\t{e}\033[0m')

    def extraer_datos_grado_marginacion_3_años(self):
        try:
            # Menores de 3 años
            data_frame_total_mujeres_matricula_menor_3_años = self.data_frame_final['Alumnos menores de 3 años mujeres']
            data_frame_total_hombres_matricula_menor_3_años = self.data_frame_final['Alumnos menores de 3 años hombres']
            # Matricula de 3 años
            data_frame_total_hombres_matricula_3_años = self.data_frame_final['Alumnos de 3 años hombres']
            data_frame_total_mujeres_matricula_3_años = self.data_frame_final['Alumnos de 3 años mujeres']

            # Grado de marginacion
            data_frame_grado_marginacion = self.data_frame_final['Grado de marginacion']
            data_frame_matricula_total = pd.concat(
                [data_frame_total_mujeres_matricula_menor_3_años,
                data_frame_total_hombres_matricula_menor_3_años,
                data_frame_total_mujeres_matricula_3_años,
                data_frame_total_hombres_matricula_3_años,
                data_frame_grado_marginacion],
                axis=1
            )
            data_frame_matricula_total['Matricula Total'] = data_frame_matricula_total[['Alumnos menores de 3 años mujeres',
                                                                     'Alumnos menores de 3 años hombres',
                                                                     'Alumnos de 3 años mujeres',
                                                                     'Alumnos de 3 años hombres']]
            resultado = data_frame_matricula_total.groupby('Grado de marginacion')['Matricula Total'].sum()

            self.datos["3"]["matricula_gm"]["muy bajo"] = resultado['Muy bajo']
            self.datos["3"]["matricula_gm"]["bajo"] = resultado['Bajo']
            self.datos["3"]["matricula_gm"]["medio"] = resultado['Medio']
            self.datos["3"]["matricula_gm"]["alto"] = resultado['Alto']
            self.datos["3"]["matricula_gm"]["muy alto"] = resultado['Muy alto']
            self.datos["3"]["matricula_gm"]["total"] = (resultado['Muy bajo'] + resultado['Bajo'] +
                                                        resultado['Medio'] + resultado['Alto'] + 
                                                        resultado['Muy alto'])
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo datos (grado de marginacion) para Atención total a la Población de 3 años para el ciclo escolar {self.ciclo_escolar.inicio}:\n\t{e}\033[0m')

    def  calcular_grado_marginacion_3_años(self):
        try:
            print(f"\033[34mCalculando grado de marginacion para atención para población de 3 años para el ciclo escolar {self.ciclo_escolar.inicio}\033[0m")
            # Atención a GM muy bajo = (matricula_gm_mb / poblacion_total) * 100
            self.datos['3']['porcentaje_matricula_gm']['muy_bajo'] = (
                self.datos['3']['matricula_gm']['muy_bajo'] / self.datos['3']['poblacion']['total'] ) * 100
            # Bajo
            self.datos['3']['porcentaje_matricula_gm']['bajo'] = (
                self.datos['3']['matricula_gm']['bajo'] / self.datos['3']['poblacion']['total'] ) * 100
            # Medio
            self.datos['3']['porcentaje_matricula_gm']['medio'] = (
                self.datos['3']['matricula_gm']['medio'] / self.datos['3']['poblacion']['total'] ) * 100
            # Alto
            self.datos['3']['porcentaje_matricula_gm']['alto'] = (
                self.datos['3']['matricula_gm']['alto'] / self.datos['3']['poblacion']['total'] ) * 100
            # Muy alto
            self.datos['3']['porcentaje_matricula_gm']['muy alto'] = (
                self.datos['3']['matricula_gm']['muy alto'] / self.datos['3']['poblacion']['total'] ) * 100
            # Total
            self.datos['3']['porcentaje_matricula_gm']['total'] = (
                self.datos['3']['matricula_gm']['total'] / self.datos['3']['poblacion']['total'] ) * 100
            
            # Se muestran los datos
            print(f'Atención grado de marginación muy bajo 3 años: {self.datos["3"]["porcentaje_matricula_gm"]["muy bajo"]}')
            print(f'Atención grado de marginación bajo 3 años: {self.datos["3"]["porcentaje_matricula_gm"]["bajo"]}')
            print(f'Atención grado de marginación medio 3 años: {self.datos["3"]["porcentaje_matricula_gm"]["medio"]}')
            print(f'Atención grado de marginación alto 3 años: {self.datos["3"]["porcentaje_matricula_gm"]["alto"]}')
            print(f'Atención grado de marginación muy alto 3 años: {self.datos["3"]["porcentaje_matricula_gm"]["muy alto"]}')
            print(f'Atención total 3 años: {self.datos["3"]["porcentaje_matricula_gm"]["total"]}')
        except Exception as e:
            print(f'\033[31mHubo un error Calculando Grado de Marginacion para Atención total a la Población de 3 años para el ciclo escolar {self.ciclo_escolar.inicio}:\n\t{e}\033[0m')
 
    def generar_grafico_grado_marginacion_atencion_individual_poblacion_3_años(self):
        try:
            print(f"\033[34mGenerando Gráfico Grado de Marginacion para Atención individual a la Población total de 3 años para el ciclo escolar {self.ciclo_escolar.inicio}\033[0m")
            # Valores ya calculados
            valores_muy_bajo = self.datos["3"]["porcentaje_matricula_gm"]["muy bajo"]
            valores_bajo = self.datos["3"]["porcentaje_matricula_gm"]["bajo"]
            valores_medio = self.datos["3"]["porcentaje_matricula_gm"]["medio"]
            valores_alto = self.datos["3"]["porcentaje_matricula_gm"]["alto"]
            valores_muy_alto = self.datos["3"]["porcentaje_matricula_gm"]["muy alto"]
            valores_sin_atencion = 100 - (valores_muy_bajo + valores_bajo + valores_medio, valores_alto, valores_muy_alto)

            # Datos para gráfica apilada
            categorias = ['Atención - Grados de marginación']
            porcentajes_muy_bajo = [valores_muy_bajo]
            porcentajes_bajo = [valores_bajo]
            porcentajes_medio = [valores_medio]
            porcentajes_alto = [valores_alto]
            porcentajes_muy_alto = [valores_muy_alto]
            porcentajes_restante = [valores_sin_atencion]

            # Paleta de colores estilo "mako"
            colores = sns.color_palette("mako", n_colors=6)

            # Creación de gráfico
            fig, ax = plt.subplots(figsize=(6, 6))

            # Apilamiento
            ax.bar(categorias, porcentajes_muy_bajo, 
                label='Muy bajo', color=colores[0])

            ax.bar(categorias, porcentajes_bajo,
                bottom=porcentajes_muy_bajo,
                label='Bajo', color=colores[1])

            ax.bar(categorias, porcentajes_medio,
                bottom=[porcentajes_muy_bajo[0] + porcentajes_bajo[0]],
                label='Medio', color=colores[2])

            ax.bar(categorias, porcentajes_alto,
                bottom=[porcentajes_muy_bajo[0] + porcentajes_bajo[0] + porcentajes_medio[0]],
                label='Alto', color=colores[3])

            ax.bar(categorias, porcentajes_muy_alto,
                bottom=[porcentajes_muy_bajo[0] + porcentajes_bajo[0] + porcentajes_medio[0] + porcentajes_alto[0]],
                label='Muy alto', color=colores[4])

            ax.bar(categorias, porcentajes_restante,
                bottom=[porcentajes_muy_bajo[0] + porcentajes_bajo[0] + porcentajes_medio[0] +
                        porcentajes_alto[0] + porcentajes_muy_alto[0]],
                label='Sin atención', color=colores[5])
            
            # Terminar las etiquetas y el modelo
            # Etiquetas
            total_marginacion = [
            porcentajes_muy_bajo[0],
            porcentajes_bajo[0],
            porcentajes_medio[0],
            porcentajes_alto[0],
            porcentajes_muy_alto[0],
            porcentajes_restante[0]
            ]
            acumulado = 0
            for i, valor in enumerate(total_marginacion):
                ax.text(0, acumulado + valor / 2, f'{valor:.1f}%', ha='center', va='center', color='white', fontsize=10)
                acumulado += valor
            # Estetica
            ax.set_ylim(0, 110)
            ax.set_ylabel('Porcentaje')
            ax.set_titile('Marginación por localidad para Atención de población de 3 años({self.ciclo_escolar.inicio})', fontsize=14)
            ax.set_xticks([[]])
            ax.legend(loc='upper right')
            # Guardar grafico
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            # Se guarda la instancia en el modelo
            instancia, _ = MarginacionPoblacion345.objects.update_or_create(
                ciclo_escolar_inicio=self.ciclo_escolar,
                porcentaje_muy_bajo = self.datos["3"]["porcentaje_matricula_gm"]["muy bajo"],
                porcentaje_bajo = self.datos["3"]["porcentaje_matricula_gm"]["bajo"],
                porcentaje_medio = self.datos["3"]["porcentaje_matricula_gm"]["medio"],
                porcentaje_alto = self.datos["3"]["porcentaje_matricula_gm"]["alto"],
                porcentaje_muy_alto = self.datos["3"]["porcentaje_matricula_gm"]["muy alto"],
                matricula_total = self.datos["3"]["matricula"]["total"],
                proyeccion_conapo_poblacion_total=self.datos["3"]["poblacion"]["total"],
                grupo_de_edad="3",
                fecha_actualizacion=date.today()
                )
            nombre_del_grafico = f"marginacion_poblacion_edad_3_{self.ciclo_escolar.inicio}_{self.ciclo_escolar.fin}.png"
            instancia.grafico.save(nombre_del_grafico, ContentFile(buffer.read()), save=True)
            plt.close(fig)
            buffer.close()
        except Exception as e:
            print(f'\033[31mHubo un error generando Gráfico Marginación por localidad para Población de 3 años para el ciclo escolar {self.ciclo_escolar.inicio}:\n\t{e}\033[0m')
    """
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 4 años⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    """
    def extraer_datos_4_años(self):
        try:
            print(f"\033[34mExtrayendo datos para Atención total a la Población de 4 años para el ciclo escolar {self.ciclo_escolar.inicio}\033[0m")
            # Matricula
            self.datos["4"]["matricula"]["mujeres"] = self.data_frame_final["Alumnos de 4 años mujeres"].sum()
            self.datos["4"]["matricula"]["hombres"] = self.data_frame_final["Alumnos de 4 años hombres"].sum()
            self.datos["4"]["matricula"]["total"] = (
                    self.datos["4"]["matricula"]["mujeres"] + self.datos["4"]["matricula"]["hombres"]
            )

            # Poblacion
            df_poblacion = self.proyeccion_poblacional
            df_poblacion = df_poblacion[df_poblacion['EDAD'].astype(int) == 4]
            df_poblacion = df_poblacion[df_poblacion['AÑO'].astype(int) == self.ciclo_escolar.inicio]

            self.datos["4"]["poblacion"]["hombres"] = df_poblacion[df_poblacion['SEXO'] == 'Hombres']['POBLACION'].sum()
            self.datos["4"]["poblacion"]["mujeres"] = df_poblacion[df_poblacion['SEXO'] == 'Mujeres']['POBLACION'].sum()
            self.datos["4"]["poblacion"]["total"] = df_poblacion['POBLACION'].sum()
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo datos para Atención total a la Población de 4 años para el ciclo escolar {self.ciclo_escolar.inicio}:\n\t{e}\033[0m')

    def calcular_atencion_4_años(self):
        try:
            print(f"\033[34mCalculando atención para población de 4 años para el ciclo escolar {self.ciclo_escolar.inicio}\033[0m")

            self.datos["4"]["atencion"]["hombres"] = (
                self.datos["4"]["matricula"]["hombres"] / self.datos["4"]["poblacion"]["total"]) * 100

            self.datos["4"]["atencion"]["mujeres"] = (
                self.datos["4"]["matricula"]["mujeres"] / self.datos["4"]["poblacion"]["total"]) * 100

            self.datos["4"]["atencion"]["total"] = (
                self.datos["4"]["matricula"]["total"] / self.datos["4"]["poblacion"]["total"]) * 100
            print(f'Atención mujeres 4 años: {self.datos["4"]["atencion"]["mujeres"]}')
            print(f'Atención hombres 4 años: {self.datos["4"]["atencion"]["hombres"]}')
            print(f'Atención total 4 años: {self.datos["4"]["atencion"]["total"]}')
        except Exception as e:
            print(f'\033[31mHubo un Error calculando atención 4 años para el ciclo escolar {self.ciclo_escolar.inicio}:\n\t{e}\033[0m')

    def generar_grafico_atencion_individual_poblacion_4_años(self):
        try:
            print(f"\033[34mGenerando Gráfico Atención individual a la Población total de 4 años para el ciclo escolar {self.ciclo_escolar.inicio}\033[0m")
            # Valores ya calculados
            valores_mujeres = self.datos["4"]["atencion"]["mujeres"]
            valores_hombres = self.datos["4"]["atencion"]["hombres"]
            valores_sin_atencion = 100 - (valores_mujeres + valores_hombres)

            # Datos para la gráfica apilada
            categorias = ['Atención']
            porcentajes_mujeres = [valores_mujeres]
            porcentajes_hombres = [valores_hombres]
            porcentajes_restante = [valores_sin_atencion]

            # Paleta de colores estilo "mako"
            colores = sns.color_palette("mako", n_colors=3)

            # Creación del gráfico
            fig, ax = plt.subplots(figsize=(6, 6))

            # Apilamiento
            ax.bar(categorias, porcentajes_mujeres, label='Mujeres', color=colores[0])
            ax.bar(categorias, porcentajes_hombres, bottom=porcentajes_mujeres, label='Hombres', color=colores[1])
            ax.bar(categorias, porcentajes_restante,
                   bottom=[porcentajes_mujeres[0] + porcentajes_hombres[0]],
                   label='Sin atención', color=colores[2])
            # Etiquetas
            total_altura = [porcentajes_mujeres[0], porcentajes_hombres[0], porcentajes_restante[0]]
            acumulado = 0
            for i, valor in enumerate(total_altura):
                ax.text(0, acumulado + valor / 2, f'{valor:.1f}%', ha='center', va='center', color='white', fontsize=10)
                acumulado += valor

            # Estética
            ax.set_ylim(0, 110)
            ax.set_ylabel('Porcentaje')
            ax.set_title(f'Atención a población de 4 años ({self.ciclo_escolar.inicio})', fontsize=14)
            ax.set_xticks([])
            ax.legend(loc='upper right')

            # Se guarda el gráfico
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)

            # Se guarda la instancia directamente en el modelo
            instancia, _ = AtencionPoblacion345.objects.update_or_create(
                ciclo_escolar_inicio = self.ciclo_escolar,
                porcentaje_atencion_hombres = self.datos["4"]["atencion"]["hombres"],
                porcentaje_atencion_mujeres = self.datos["4"]["atencion"]["mujeres"],
                porcentaje_atencion_total = self.datos["4"]["atencion"]["total"],
                matricula_hombres = self.datos["4"]["matricula"]["hombres"],
                matricula_mujeres = self.datos["4"]["matricula"]["mujeres"],
                matricula_total = self.datos["4"]["matricula"]["total"],
                proyeccion_conapo_poblacion_hombres = self.datos["4"]["poblacion"]["hombres"],
                proyeccion_conapo_poblacion_mujeres = self.datos["4"]["poblacion"]["mujeres"],
                proyeccion_conapo_poblacion_total = self.datos["4"]["poblacion"]["total"],
                grupo_de_edad="4",
                fecha_actualizacion = date.today()
            )
            nombre_del_grafico = f"atencion_poblacion_edad_4_{self.ciclo_escolar.inicio}_{self.ciclo_escolar.fin}.png"
            instancia.grafico.save(nombre_del_grafico, ContentFile(buffer.read()), save=True)
            plt.close(fig)
            buffer.close()
        except Exception as e:
            print(f'\033[31mHubo un error generando Gráfico Atención total a la Población de 4 años para el ciclo escolar {self.ciclo_escolar.inicio}:\n\t{e}\033[0m')

    """
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 5 años⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    """
    def extraer_datos_5_años(self):
        try:
            print(
                f"\033[34mExtrayendo datos para Atención total a la Población de 5 años para el ciclo escolar {self.ciclo_escolar.inicio}\033[0m")

            # Matrícula
            self.datos["5"]["matricula"]["mujeres"] = self.data_frame_final['Alumnos de 5 años mujeres'].sum()
            self.datos["5"]["matricula"]["hombres"] = self.data_frame_final['Alumnos de 5 años hombres'].sum()
            self.datos["5"]["matricula"]["total"] = (
                self.datos["5"]["matricula"]["mujeres"] + self.datos["5"]["matricula"]["hombres"]
            )

            # Población
            df_poblacion = self.proyeccion_poblacional
            df_poblacion = df_poblacion[df_poblacion['EDAD'].astype(int) == 5]
            df_poblacion = df_poblacion[df_poblacion['AÑO'].astype(int) == self.ciclo_escolar.inicio]

            self.datos["5"]["poblacion"]["hombres"] = df_poblacion[df_poblacion['SEXO'] == 'Hombres']['POBLACION'].sum()
            self.datos["5"]["poblacion"]["mujeres"] = df_poblacion[df_poblacion['SEXO'] == 'Mujeres']['POBLACION'].sum()
            self.datos["5"]["poblacion"]["total"] = df_poblacion['POBLACION'].sum()
        except Exception as e:
            print(f'\033[31mHubo un error extrayendo datos para Atención total a la Población de 5 años para el ciclo escolar {self.ciclo_escolar.inicio}:\n\t{e}\033[0m')


    def calcular_atencion_5_años(self):
        try:
            print(f"\033[34mCalculando atención para población de 5 años\033[0m")
            self.datos["5"]["atencion"]["hombres"] = (
                self.datos["5"]["matricula"]["hombres"] / self.datos["5"]["poblacion"]["total"] ) * 100

            self.datos["5"]["atencion"]["mujeres"] = (
                self.datos["5"]["matricula"]["mujeres"] /self.datos["5"]["poblacion"]["total"]) * 100

            self.datos["5"]["atencion"]["total"] = (
                self.datos["5"]["matricula"]["total"] / self.datos["5"]["poblacion"]["total"]) * 100

            print(f'Atención mujeres 5 años: {self.datos["5"]["atencion"]["mujeres"]}')
            print(f'Atención hombres 5 años: {self.datos["5"]["atencion"]["hombres"]}')
            print(f'Atención total 5 años: {self.datos["5"]["atencion"]["total"]}')
        except Exception as e:
            print(f'\033[31mError calculando atención 5 años: {e}\033[0m')

    def generar_grafico_atencion_individual_poblacion_5_años(self):
        try:
            print(f"\033[34mGenerando Gráfico Atención individual a la Población total de 5 años para el ciclo escolar {self.ciclo_escolar.inicio}\033[0m")
            # Valores ya calculados
            valores_mujeres = self.datos["5"]["atencion"]["mujeres"]
            valores_hombres = self.datos["5"]["atencion"]["hombres"]
            valores_sin_atencion = 100 - (valores_mujeres + valores_hombres)

            # Datos para la gráfica apilada
            categorias = ["Atención"]
            porcentajes_mujeres = [valores_mujeres]
            porcentajes_hombres = [valores_hombres]
            porcentajes_restante = [valores_sin_atencion]

            # Paleta de colores estilo "mako"
            colores = sns.color_palette("mako", n_colors=3)

            # Creación del gráfico
            fig, ax = plt.subplots(figsize=(6, 6))

            # Apilamiento
            ax.bar(categorias, porcentajes_mujeres, label='Mujeres', color=colores[0])
            ax.bar(categorias, porcentajes_hombres, bottom=porcentajes_mujeres, label='Hombres', color=colores[1])
            ax.bar(categorias, porcentajes_restante,
                   bottom=[porcentajes_mujeres[0] + porcentajes_hombres[0]],
                   label='Sin atención', color=colores[2])

            # Etiquetas
            total_altura = [porcentajes_mujeres[0], porcentajes_hombres[0], porcentajes_restante[0]]
            acumulado = 0
            for i, valor in enumerate(total_altura):
                ax.text(0, acumulado + valor / 2, f'{valor:.1f}%', ha='center', va='center', color='white', fontsize=10)
                acumulado += valor

            # Estética
            ax.set_ylim(0, 110)
            ax.set_ylabel('Porcentaje')
            ax.set_title(f'Atención a población de 5 años ({self.ciclo_escolar.inicio})', fontsize=14)
            ax.set_xticks([])
            ax.legend(loc='upper right')

            # Se guarda el gráfico}
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)

            # Se guarda la instancia directamente en el modelo
            instancia, _ = AtencionPoblacion345.objects.update_or_create(
                ciclo_escolar_inicio = self.ciclo_escolar,
                porcentaje_atencion_hombres = self.datos["5"]["atencion"]["hombres"],
                porcentaje_atencion_mujeres = self.datos["5"]["atencion"]["mujeres"],
                porcentaje_atencion_total = self.datos["5"]["atencion"]["total"],
                matricula_hombres = self.datos["5"]["matricula"]["hombres"],
                matricula_mujeres = self.datos["5"]["matricula"]["mujeres"],
                matricula_total = self.datos["5"]["matricula"]["total"],
                proyeccion_conapo_poblacion_hombres = self.datos["5"]["poblacion"]["hombres"],
                proyeccion_conapo_poblacion_mujeres = self.datos["5"]["poblacion"]["mujeres"],
                proyeccion_conapo_poblacion_total = self.datos["5"]["poblacion"]["total"],
                grupo_de_edad="5",
                fecha_actualizacion = date.today()
            )
            nombre_del_grafico = f"atencion_poblacion_edad_5_{self.ciclo_escolar.inicio}_{self.ciclo_escolar.fin}.png"
            instancia.grafico.save(nombre_del_grafico, ContentFile(buffer.read()), save=True)
            plt.close(fig)
            buffer.close()
        except Exception as e:
            print(f'\033[31mHubo un error generando Gráfico Atención total a la Población de 5 años para el ciclo escolar {self.ciclo_escolar.inicio}:\n\t{e}\033[0m')

    """
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ Gráfico de multiples ciclos escolares⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ ⋆⁺₊⋆ 
    """

    def generar_grafico_atencion_multiple_edad_3(self):
        try:
            print("\033[1mGenerando gráfico de atención a población de 3 años para múltiples ciclos escolares...\033[0m")
            qs = list(self.modelo_atencion_poblacion345
                      .filter(grupo_de_edad="3")
                      .order_by('-ciclo_escolar_inicio__inicio')[:5])

            qs = list(reversed(qs))  # De más antiguo a más reciente
            total_registros = len(qs)

            if total_registros == 0:
                print("No hay datos disponibles para graficar.")
                return

            registros = []
            primer_ciclo = None
            ultimo_ciclo = None

            for i, instancia in enumerate(qs):
                año = str(instancia.ciclo_escolar_inicio.inicio)  # Etiquetas categóricas

                mujeres = float(instancia.porcentaje_atencion_mujeres or 0)
                hombres = float(instancia.porcentaje_atencion_hombres or 0)
                sin_atencion = max(0.0, 100.0 - (mujeres + hombres))

                registros.append({"Ciclo escolar": año, "Grupo": "Mujeres", "Porcentaje": mujeres})
                registros.append({"Ciclo escolar": año, "Grupo": "Hombres", "Porcentaje": hombres})
                registros.append({"Ciclo escolar": año, "Grupo": "Sin atención", "Porcentaje": sin_atencion})

                if i == 0:
                    primer_ciclo = instancia.ciclo_escolar_inicio
                elif i == (total_registros - 1):
                    ultimo_ciclo = instancia.ciclo_escolar_inicio

            # Crear DataFrame
            df = pd.DataFrame(registros)

            # Verificación intermedia (puedes dejar esto temporalmente)
            print("DataFrame generado:")
            print(df.head())

            # Asegurar tipos
            df["Porcentaje"] = pd.to_numeric(df["Porcentaje"], errors='coerce')
            df.dropna(subset=["Porcentaje"], inplace=True)

            if df.empty:
                print("El DataFrame está vacío después de limpiar los datos.")
                return

            df["Ciclo escolar"] = pd.Categorical(df["Ciclo escolar"], ordered=True,
                                                 categories=sorted(df["Ciclo escolar"].unique()))
            df["Grupo"] = pd.Categorical(df["Grupo"], categories=["Mujeres", "Hombres", "Sin atención"], ordered=True)

            pivot = df.pivot(index="Ciclo escolar", columns="Grupo", values="Porcentaje").fillna(0)

            # === Crear gráfico apilado ===
            plt.figure(figsize=(10, 6))
            colores = sns.color_palette("mako", n_colors=3)
            ax = pivot.plot(kind="bar", stacked=True, color=colores, edgecolor="white")

            ax.set_ylabel("Porcentaje de atención")
            ax.set_xlabel("Ciclo escolar")
            ax.set_title(f"Atención a población de 3 años")
            ax.set_ylim(0, 110)
            ax.legend(title="Grupo", bbox_to_anchor=(1.05, 1), loc='upper left')

            # Etiquetas de porcentaje
            for container in ax.containers:
                ax.bar_label(container, fmt='%.1f%%', label_type='center')

            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)

            instancia, _ = graficos_multiples.objects.update_or_create(
                primer_ciclo_escolar = primer_ciclo,
                ultimo_ciclo_escolar = ultimo_ciclo,
                indicador = "AE3",
                fecha_actualizacion = date.today()
            )
            nombre = f"atencion_poblacion_edad_3_{primer_ciclo}_{ultimo_ciclo}.png"
            instancia.grafico.save(nombre, ContentFile(buffer.read()), save=True)

            plt.close()
            buffer.close()

        except Exception as e:
            print(f"\033[31mError generando gráfico múltiple para 3 años:\n\t{e}\033[0m")

    def generar_grafico_atencion_multiple_edad_4(self):
        try:
            print("\033[1mGenerando gráfico de atención a población de 4 años para múltiples ciclos escolares...\033[0m")
            qs = list(self.modelo_atencion_poblacion345
                      .filter(grupo_de_edad="4")
                      .order_by('-ciclo_escolar_inicio__inicio')[:5])

            qs = list(reversed(qs))  # De más antiguo a más reciente
            total_registros = len(qs)

            if total_registros == 0:
                print("No hay datos disponibles para graficar.")
                return

            registros = []
            primer_ciclo = None
            ultimo_ciclo = None

            for i, instancia in enumerate(qs):
                año = str(instancia.ciclo_escolar_inicio.inicio)  # Etiquetas categóricas

                mujeres = float(instancia.porcentaje_atencion_mujeres or 0)
                hombres = float(instancia.porcentaje_atencion_hombres or 0)
                sin_atencion = max(0.0, 100.0 - (mujeres + hombres))

                registros.append({"Ciclo escolar": año, "Grupo": "Mujeres", "Porcentaje": mujeres})
                registros.append({"Ciclo escolar": año, "Grupo": "Hombres", "Porcentaje": hombres})
                registros.append({"Ciclo escolar": año, "Grupo": "Sin atención", "Porcentaje": sin_atencion})

                if i == 0:
                    primer_ciclo = instancia.ciclo_escolar_inicio
                elif i == (total_registros - 1):
                    ultimo_ciclo = instancia.ciclo_escolar_inicio

            # Crear DataFrame
            df = pd.DataFrame(registros)

            # Verificación intermedia (puedes dejar esto temporalmente)
            print("DataFrame generado:")
            print(df.head())

            # Asegurar tipos
            df["Porcentaje"] = pd.to_numeric(df["Porcentaje"], errors='coerce')
            df.dropna(subset=["Porcentaje"], inplace=True)

            if df.empty:
                print("El DataFrame está vacío después de limpiar los datos.")
                return

            df["Ciclo escolar"] = pd.Categorical(df["Ciclo escolar"], ordered=True,
                                                 categories=sorted(df["Ciclo escolar"].unique()))
            df["Grupo"] = pd.Categorical(df["Grupo"], categories=["Mujeres", "Hombres", "Sin atención"], ordered=True)

            pivot = df.pivot(index="Ciclo escolar", columns="Grupo", values="Porcentaje").fillna(0)

            # === Crear gráfico apilado ===
            plt.figure(figsize=(10, 6))
            colores = sns.color_palette("mako", n_colors=3)
            ax = pivot.plot(kind="bar", stacked=True, color=colores, edgecolor="white")

            ax.set_ylabel("Porcentaje de atención")
            ax.set_xlabel("Ciclo escolar")
            ax.set_title(f"Atención a población de 4 años")
            ax.set_ylim(0, 110)
            ax.legend(title="Grupo", bbox_to_anchor=(1.05, 1), loc='upper left')

            # Etiquetas de porcentaje
            for container in ax.containers:
                ax.bar_label(container, fmt='%.1f%%', label_type='center')

            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)

            instancia, _ = graficos_multiples.objects.update_or_create(
                primer_ciclo_escolar = primer_ciclo,
                ultimo_ciclo_escolar = ultimo_ciclo,
                indicador = "AE4",
                fecha_actualizacion = date.today()
            )
            nombre = f"atencion_poblacion_edad_4_{primer_ciclo}_{ultimo_ciclo}.png"
            instancia.grafico.save(nombre, ContentFile(buffer.read()), save=True)

            plt.close()
            buffer.close()

        except Exception as e:
            print(f"\033[31mError generando gráfico múltiple para 4 años:\n\t{e}\033[0m")

    def generar_grafico_atencion_multiple_edad_5(self):
        try:
            print("\033[1mGenerando gráfico de atención a población de 5 años para múltiples ciclos escolares...\033[0m")
            qs = list(self.modelo_atencion_poblacion345
                      .filter(grupo_de_edad="5")
                      .order_by('-ciclo_escolar_inicio__inicio')[:5])

            qs = list(reversed(qs))  # De más antiguo a más reciente
            total_registros = len(qs)

            if total_registros == 0:
                print("No hay datos disponibles para graficar.")
                return

            registros = []
            primer_ciclo = None
            ultimo_ciclo = None

            for i, instancia in enumerate(qs):
                año = str(instancia.ciclo_escolar_inicio.inicio)  # Etiquetas categóricas

                mujeres = float(instancia.porcentaje_atencion_mujeres or 0)
                hombres = float(instancia.porcentaje_atencion_hombres or 0)
                sin_atencion = max(0.0, 100.0 - (mujeres + hombres))

                registros.append({"Ciclo escolar": año, "Grupo": "Mujeres", "Porcentaje": mujeres})
                registros.append({"Ciclo escolar": año, "Grupo": "Hombres", "Porcentaje": hombres})
                registros.append({"Ciclo escolar": año, "Grupo": "Sin atención", "Porcentaje": sin_atencion})

                if i == 0:
                    primer_ciclo = instancia.ciclo_escolar_inicio
                elif i == (total_registros - 1):
                    ultimo_ciclo = instancia.ciclo_escolar_inicio

            # Crear DataFrame
            df = pd.DataFrame(registros)

            # Verificación intermedia (puedes dejar esto temporalmente)
            print("DataFrame generado:")
            print(df.head())

            # Asegurar tipos
            df["Porcentaje"] = pd.to_numeric(df["Porcentaje"], errors='coerce')
            df.dropna(subset=["Porcentaje"], inplace=True)

            if df.empty:
                print("El DataFrame está vacío después de limpiar los datos.")
                return

            df["Ciclo escolar"] = pd.Categorical(df["Ciclo escolar"], ordered=True,
                                                 categories=sorted(df["Ciclo escolar"].unique()))
            df["Grupo"] = pd.Categorical(df["Grupo"], categories=["Mujeres", "Hombres", "Sin atención"], ordered=True)

            pivot = df.pivot(index="Ciclo escolar", columns="Grupo", values="Porcentaje").fillna(0)

            # === Crear gráfico apilado ===
            plt.figure(figsize=(10, 6))
            colores = sns.color_palette("mako", n_colors=3)
            ax = pivot.plot(kind="bar", stacked=True, color=colores, edgecolor="white")

            ax.set_ylabel("Porcentaje de atención")
            ax.set_xlabel("Ciclo escolar")
            ax.set_title(f"Atención a población de 5 años")
            ax.set_ylim(0, 110)
            ax.legend(title="Grupo", bbox_to_anchor=(1.05, 1), loc='upper left')

            # Etiquetas de porcentaje
            for container in ax.containers:
                ax.bar_label(container, fmt='%.1f%%', label_type='center')

            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)

            instancia, _ = graficos_multiples.objects.update_or_create(
                primer_ciclo_escolar = primer_ciclo,
                ultimo_ciclo_escolar = ultimo_ciclo,
                indicador = "AE5",
                fecha_actualizacion = date.today()
            )
            nombre = f"atencion_poblacion_edad_5_{primer_ciclo}_{ultimo_ciclo}.png"
            instancia.grafico.save(nombre, ContentFile(buffer.read()), save=True)

            plt.close()
            buffer.close()

        except Exception as e:
            print(f"\033[31mError generando gráfico múltiple para 5 años:\n\t{e}\033[0m")

def principal(ciclo_escolar_solicitado, datos_preescolar, proyeccion_poblacional):
    # Es importante recalcar que el calculo se hace con CicloEscolar(N), pero el resultado es para CicloEscolar(N-1)
    calculadora = CalculadoraCoberturaPreescolar(ciclo_escolar_solicitado, datos_preescolar, proyeccion_poblacional)
    # 3 años
    calculadora.extraer_datos_3_años()
    calculadora.calcular_atencion_3_años()
    calculadora.generar_grafico_atencion_individual_poblacion_3_años()
    calculadora.extraer_datos_grado_marginacion_3_años()
    calculadora.calcular_grado_marginacion_3_años()
    calculadora.generar_grafico_grado_marginacion_atencion_individual_poblacion_3_años()
    # 4 años
    calculadora.extraer_datos_4_años()
    calculadora.calcular_atencion_4_años()
    calculadora.generar_grafico_atencion_individual_poblacion_4_años()
    # 5 años
    calculadora.extraer_datos_5_años()
    calculadora.calcular_atencion_5_años()
    calculadora.generar_grafico_atencion_individual_poblacion_5_años()

# TODO: Generar logica para actualizar registros ya existentes

def graficos_multiples_ciclos(ciclo_escolar_solicitado, datos_preescolar, proyeccion_poblacional):
    calculadora = CalculadoraCoberturaPreescolar(ciclo_escolar_solicitado, datos_preescolar, proyeccion_poblacional)
    calculadora.generar_grafico_atencion_multiple_edad_3()
    calculadora.generar_grafico_atencion_multiple_edad_4()
    calculadora.generar_grafico_atencion_multiple_edad_5()