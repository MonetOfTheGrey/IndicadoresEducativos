from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import F

@login_required
def panel_datos(request):
    return render(request, 'panel_datos.html')

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
    if request.method == 'POST':
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

        total_filas = int(request.POST.get('total_filas', 0))

        for i in range(1, total_filas + 1):

            nombre = request.POST.get(f'nombre_{i}')
            ciclo_escolar_inicio = request.POST.get(f'ciclo_{i}')
            fecha = request.POST.get(f'fecha_{i}')
            archivo = request.FILES.get(f'archivo_{i}')

            if archivo:
                # Buscar modelo correspondiente
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
                        # Si no se encuentra el ciclo, ignorar esa fila o registrar un error
                        print("No se encontro ciclo escolar")
                        return redirect(agregar_911)

        return redirect(agregar_911)

    return redirect(agregar_911)
    