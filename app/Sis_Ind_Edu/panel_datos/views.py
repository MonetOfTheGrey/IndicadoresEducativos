from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import F

@login_required
def limpiar_proyecciones_poblacionales(request):
    if request.method == 'POST':
        try:
            # importar el script para ejecutarlo
            from panel_datos.scripts import limpiar_proyecciones_poblacionales as script_de_limpieza
            # Ejecutar la funcion principal
            script_de_limpieza.principal(request.user)
            return redirect('panel_datos')
        except Exception as e:
            print(f'\033[31mError importando y ejecutando "limpiar_proyecionesPoblacionales"\n{e}\033[0m')
            return render(request, 'panel_datos.html', {'error': str(e)})
    else:
        print(request.method)
        return render(request, 'panel_datos.html')

@login_required
def actualizar_cobertura_escolar(request):
    if request.method == 'POST':
        try:
            # Se importa el script para ejecutarlo
            from panel_datos.scripts import cobertura_escolar as script_cobertura_escolar
            # Se ejecuta la funcion principal
            script_cobertura_escolar.principal()
            return redirect('panel_datos')
        except Exception as e:
            print(f'\033[31mError importando y ejecutando "cobertura_escolar.py"\n{e}\033[0m')
            return render(request, 'panel_datos.html', {'error': str(e)})
    else:
        print(request.method)
        return render(request, 'panel_datos.html')

@login_required
def panel_datos(request):
    return render(request, 'panel_datos.html')

@login_required
def agregar_conapo(request):
    # ----------------8<-------------[ cut here ]------------------
    # aqui se generan los archivos de CONAPO
    archivos_conapo = [
        {'nombre': 'Proyecciones poblacionales a mediados de año 1950-2070', "modelo": ProyeccionesPoblacionales},
        {'nombre': 'Indices de Marginación por Localidad 2020', "modelo": MarginacionLocalidad},
    ]
    # ----------------8<-------------[ cut here ]------------------
    # Contexto de las bases ya existentes en el sistema
    proyecciones_existentes = list(
        ProyeccionesPoblacionales.objects
        .select_related('actualizado_por')
        .annotate(actualizado_por_nombre=F('actualizado_por__first_name'))
        .values('nombre', 'fecha_actualizacion', 'actualizado_por', 'actualizado_por_nombre')
    )
    marginacion_por_localidad_existente = list(
        MarginacionLocalidad.objects
        .select_related('actualizado_por')
        .annotate(actualizado_por_nombre=F('actualizado_por__first_name'))
        .values('nombre', 'fecha_actualizacion', 'actualizado_por', 'actualizado_por_nombre')
    )
    # ----------------8<-------------[ cut here ]------------------
    contexto = {
        'archivos_conapo': archivos_conapo,
        'proyecciones_existentes': proyecciones_existentes,
        'marginacion_por_localidad_existente': marginacion_por_localidad_existente,
    }
    return render(request, 'agregar_conapo.html', contexto)

@login_required
def subir_archivos_conapo(request):
    if request.method == 'POST':
        archivos_conapo = [
            {'nombre': 'Proyecciones poblacionales a mediados de año 1950-2070', "modelo": ProyeccionesPoblacionales},
            {'nombre': 'Indices de Marginación por Localidad 2020', "modelo": MarginacionLocalidad},
        ]

        total_filas = int(request.POST.get('total_filas', 0))

        for i in range(1, total_filas + 1):

            nombre = request.POST.get(f'nombre_{i}')
            fecha = request.POST.get(f'fecha_{i}')
            archivo = request.FILES.get(f'archivo_{i}')

            if archivo:
                # Buscar modelo correspondiente
                modelo = next((n['modelo'] for n in archivos_conapo if n['nombre'] == nombre), None)
                if modelo:
                    try:
                        modelo.objects.create(
                            actualizado_por=request.user,
                            nombre=nombre,
                            fecha_actualizacion=fecha,
                            archivo=archivo
                        )
                    except Exception as e:
                        # Si no se encuentra el ciclo, ignorar esa fila o registrar un error
                        print("Hubo un error:\n")
                        print(e)
                        return redirect(agregar_conapo)

        return redirect(agregar_conapo)

    return redirect(agregar_conapo)

@login_required
def agregar_911(request):
    # ----------------8<-------------[ cut here ]------------------
    # aqui se generan los niveles educativos
    niveles = [
        {'nombre': 'Inicial', "modelo": EducacionInicial},
        {'nombre': 'Inicial Comunitaria Rural', "modelo": EducacionInicial},

        {'nombre': 'Preescolar', "modelo": EducacionPreescolar},
        {'nombre': 'Preescolar Comunitaria Rural', "modelo": EducacionPreescolar},

        {'nombre': 'Primaria', "modelo": EducacionPrimaria},
        {'nombre': 'Primaria Comunitaria Rural', "modelo": EducacionPrimaria},

        {'nombre': 'Secundaria', "modelo": EducacionSecundaria},
        {'nombre': 'Secundaria Comunitaria Rural', "modelo":EducacionSecundaria},

        {'nombre': 'Bachillerato General', "modelo": EducacionMediaSuperior},
        {'nombre': 'Bachillerato Carrera', "modelo": EducacionMediaSuperior},
        {'nombre': 'Bachillerato Plantel', "modelo": EducacionMediaSuperior},

        {'nombre': 'Superior Carrera', "modelo": EducacionSuperior},
        {'nombre': 'Superior Escuela', "modelo": EducacionSuperior},
    ]
    # ----------------8<-------------[ cut here ]------------------
    # Contexto de las bases ya existentes en el sistema
    bases_inicial = list(
        EducacionInicial.objects
        .select_related('actualizado_por')
        .annotate(actualizado_por_nombre=F('actualizado_por__first_name'))
        .values('nombre', 'ciclo_escolar_inicio', 'fecha_actualizacion', 'actualizado_por', 'actualizado_por_nombre')
    )

    bases_preescolar = list(
        EducacionPreescolar.objects
        .select_related('actualizado_por')
        .annotate(actualizado_por_nombre=F('actualizado_por__first_name'))
        .values('nombre', 'ciclo_escolar_inicio', 'fecha_actualizacion', 'actualizado_por', 'actualizado_por_nombre')
    )

    bases_primaria = list(
        EducacionPrimaria.objects
        .select_related('actualizado_por')
        .annotate(actualizado_por_nombre=F('actualizado_por__first_name'))
        .values('nombre', 'ciclo_escolar_inicio', 'fecha_actualizacion', 'actualizado_por', 'actualizado_por_nombre')
    )

    bases_secundaria = list(
        EducacionSecundaria.objects
        .select_related('actualizado_por')
        .annotate(actualizado_por_nombre=F('actualizado_por__first_name'))
        .values('nombre', 'ciclo_escolar_inicio', 'fecha_actualizacion', 'actualizado_por', 'actualizado_por_nombre')
    )

    bases_media_superior = list(
        EducacionMediaSuperior.objects
        .select_related('actualizado_por')
        .annotate(actualizado_por_nombre=F('actualizado_por__first_name'))
        .values('nombre', 'ciclo_escolar_inicio', 'fecha_actualizacion', 'actualizado_por', 'actualizado_por_nombre')
    )

    bases_superior = list(
        EducacionSuperior.objects
        .select_related('actualizado_por')
        .annotate(actualizado_por_nombre=F('actualizado_por__first_name'))
        .values('nombre', 'ciclo_escolar_inicio', 'fecha_actualizacion', 'actualizado_por', 'actualizado_por_nombre')
    )

    # ----------------8<-------------[ cut here ]------------------

    contexto = {
        'niveles': niveles,
        'ciclos_escolares' : CiclosEscolares.objects.all(),
        'bases_inicial': bases_inicial,
        'bases_preescolar': bases_preescolar,
        'bases_primaria': bases_primaria,
        'bases_secundaria': bases_secundaria,
        'bases_media_superior': bases_media_superior,
        'bases_superior': bases_superior,
    }
    return render(request, 'agregar911.html', contexto)

@login_required
def subir_archivos_911(request):
    niveles = [
        {'nombre': 'Inicial', "modelo": EducacionInicial},
        {'nombre': 'Inicial Comunitaria Rural', "modelo": EducacionInicial},
        {'nombre': 'Preescolar', "modelo": EducacionPreescolar},
        {'nombre': 'Preescolar Comunitaria Rural', "modelo": EducacionPreescolar},
        {'nombre': 'Primaria', "modelo": EducacionPrimaria},
        {'nombre': 'Primaria Comunitaria Rural', "modelo": EducacionPrimaria},
        {'nombre': 'Secundaria', "modelo": EducacionSecundaria},
        {'nombre': 'Secundaria Comunitaria Rural', "modelo": EducacionSecundaria},
        {'nombre': 'Bachillerato General', "modelo": EducacionMediaSuperior},
        {'nombre': 'Bachillerato Carrera', "modelo": EducacionMediaSuperior},
        {'nombre': 'Bachillerato Plantel', "modelo": EducacionMediaSuperior},
        {'nombre': 'Superior Carrera', "modelo": EducacionSuperior},
        {'nombre': 'Superior Escuela', "modelo": EducacionSuperior},
    ]

    ciclos = CiclosEscolares.objects.all().order_by("-inicio")
    errores = []

    # POST: agregar archivos
    if request.method == 'POST':
        total_filas = int(request.POST.get('total_filas', len(niveles)))

        for i in range(1, total_filas + 1):
            nombre = request.POST.get(f'nombre_{i}')
            ciclo_escolar_inicio = request.POST.get(f'ciclo_{i}')
            fecha = request.POST.get(f'fecha_{i}')
            archivo = request.FILES.get(f'archivo_{i}')

            if not (nombre or ciclo_escolar_inicio or fecha or archivo):
                continue
            if not (nombre and ciclo_escolar_inicio and fecha and archivo):
                errores.append(f"Fila {i}: todos los campos (ciclo, fecha y archivo) son obligatorios.")
                continue

            modelo = next((n['modelo'] for n in niveles if n['nombre'] == nombre), None)
            if modelo:
                try:
                    ciclo = CiclosEscolares.objects.get(inicio=ciclo_escolar_inicio)
                    modelo.objects.create(
                        actualizado_por=request.user,
                        nombre=nombre,
                        ciclo_escolar_inicio=ciclo,
                        fecha_actualizacion=fecha,
                        archivo=archivo
                    )
                except CiclosEscolares.DoesNotExist:
                    errores.append(f"Fila {i}: ciclo escolar '{ciclo_escolar_inicio}' no existe.")

    # Siempre recargar las bases con datos actualizados
    context_bases = {
        "bases_inicial": EducacionInicial.objects.select_related('actualizado_por').all(),
        "bases_preescolar": EducacionPreescolar.objects.select_related('actualizado_por').all(),
        "bases_primaria": EducacionPrimaria.objects.select_related('actualizado_por').all(),
        "bases_secundaria": EducacionSecundaria.objects.select_related('actualizado_por').all(),
        "bases_media_superior": EducacionMediaSuperior.objects.select_related('actualizado_por').all(),
        "bases_superior": EducacionSuperior.objects.select_related('actualizado_por').all(),
    }

    # Generar atributo temporal 'usuario_nombre' para mostrar en el template TODO: revisar si eliminar esto no lo rompe
    for bases in context_bases.values():
        for base in bases:
            user = getattr(base, "actualizado_por", None)
            if user and hasattr(user, "username"):
                nombre_completo = f"{user.first_name} {user.last_name}".strip()
                base.usuario_nombre = nombre_completo if nombre_completo else user.username
            else:
                base.usuario_nombre = "Usuario no asignado"

    return render(
        request,
        'agregar911.html',
        {
            "niveles": niveles,
            "ciclos_escolares": ciclos,
            "errores": errores,
            **context_bases,
        }
    )

indicadores_formulario = [
        # Indicadores de Atención a Edades 3, 4 y 5
        {"indicador": "AE3", "nombre": "Atención Edad 3 años", "modelo": IndicadorDefinicion},
        {"indicador": "AE4", "nombre": "Atención Edad 4 años", "modelo": IndicadorDefinicion},
        {"indicador": "AE5", "nombre": "Atención Edad 5 años", "modelo": IndicadorDefinicion},
    ]

@login_required
def agregar_definicion(request):

    contexto = {
        'indicadores_formulario': indicadores_formulario,
        'indicadores_existentes': IndicadorDefinicion.objects.all()
    }
    return render(request, 'agregar_definicion.html', contexto)

@login_required
def subir_definicion(request):

    errores = []

    if request.method == "POST":
        total_filas = int(request.POST.get("total_filas", len(indicadores_formulario)))

        for i in range(1, total_filas + 1):
            indicador = request.POST.get(f"indicador_{i}")
            definicion = request.POST.get(f"definicion_{i}")

            print(f"Fila {i}: indicador={indicador}, definicion={definicion}")

            if not (indicador and definicion):
                errores.append(f"Fila {i}: faltan datos.")
                continue

            try:
                obj, creado = IndicadorDefinicion.objects.update_or_create(
                    indicador=indicador,
                    defaults={"definicion": definicion}
                )
                print(f" → {'CREADO' if creado else 'ACTUALIZADO'}: {obj.indicador}")
            except Exception as e:
                errores.append(f"Error al guardar '{indicador}': {e}")

    contexto = {
        "indicadores_formulario": indicadores_formulario,
        "indicadores_existentes": IndicadorDefinicion.objects.all(),
        "errores": errores,
    }

    return render(request, "agregar_definicion.html", contexto)

@login_required
def agregar_interpretacion(request):

    contexto = {
        'indicadores_formulario': indicadores_formulario,
        'indicadores_existentes': interpretaciones_indicadores.objects.all()
    }
    return render(request, 'agregar_interpretacion.html', contexto)

@login_required
def subir_interpretacion(request):

    errores = []

    if request.method == "POST":
        total_filas = int(request.POST.get("total_filas", len(indicadores_formulario)))

        for i in range(1, total_filas + 1):
            indicador = request.POST.get(f"indicador_{i}")
            interpretacion = request.POST.get(f"interpretacion_{i}")

            print(f"Fila {i}: indicadores={indicador}, interpretacion={interpretacion}")

            if not (indicador and interpretacion):
                errores.append(f"Fila {i}: faltan datos.")
                continue

            try:
                obj, creado = interpretaciones_indicadores.objects.update_or_create(
                    indicador = indicador,
                    defaults={"interpretacion": interpretacion}
                )
                print(f" → {'CREADO' if creado else 'ACTUALIZADO'}: {obj.indicador}")
            except Exception as e:
                errores.append(f"Error al guardar '{indicador}': {e}")
        
        for error in errores:
            print (error)

        contexto = {
            "indicadores_formulario": indicadores_formulario,
            "indicadores_existentes": interpretaciones_indicadores.objects.all(),
            "errores": errores,
        }

        return render(request, "agregar_interpretacion.html", contexto)
    

@login_required
def agregar_algoritmo(request):
    contexto = {
        'indicadores_formulario': indicadores_formulario,
        'algoritmos_indicadores': algoritmos_indicadores.objects.all()
    }
    return render(request, 'agregar_algoritmo.html', contexto)

@login_required
def subir_algoritmo(request):
    errores = []
    if request.method == "POST":
        total_filas = int(request.POST.get("total_filas", len(indicadores_formulario)))

        for i in range(1, total_filas + 1):
            indicador = request.POST.get(f"indicador_{i}")
            algoritmo = request.FILES.get(f"archivo_{i}")

            print(f"Fila{i}: indicadores={indicador}, algoritmo={algoritmo}")

            if not (indicador and algoritmo):
                errores.append(f"Fila {i}: faltan datos.")
                continue

            try:
                obj, creado = algoritmos_indicadores.objects.update_or_create(
                    indicador = indicador,
                    defaults={"algoritmo": algoritmo}
                )
                print(f" → {'CREADO' if creado else 'ACTUALIZADO'}: {obj.indicador}")
            except Exception as e:
                errores.append(f"Error al guardar '{indicador}': {e}")
        for error in errores:
            print(error)
        
        contexto = {
            "indicadores_formulario": indicadores_formulario,
            "algoritmo_existente": algoritmos_indicadores.objects.all(),
            "errores": errores,
        }
        return render(request, "agregar_algoritmo.html", contexto)