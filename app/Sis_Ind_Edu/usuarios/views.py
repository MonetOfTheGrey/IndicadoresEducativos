from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from panel_datos.models import AtencionPoblacion345, graficos_multiples, CiclosEscolares, MarginacionPoblacion345
from panel_datos.models import IndicadorDefinicion, interpretaciones_indicadores, algoritmos_indicadores
from django.db.models import Q
# Create your views here.
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # esta línea captura la URL original
            next_url = request.POST.get('next')
            # si no había 'next', redirige a '/'
            return redirect(next_url or '/') 
        else:
 
            return render(request, 'iniciar_sesion.html', {'error_message': 'Credenciales inválidas.'})
    else:
        return render(request, 'iniciar_sesion.html')
    

def blank(request):
    indicador_seleccionado = request.GET.get("indicador")
    ciclo_seleccionado = request.GET.get("ciclo")

    ciclos_escolares = CiclosEscolares.objects.all().order_by('-inicio')

    indicadores = {
        "AE3": "Atención Edad 3 años",
        "AE4": "Atención Edad 4 años",
        "AE5": "Atención Edad 5 años",
    }

    indicador_a_edad = {
        "AE3": "3",
        "AE4": "4",
        "AE5": "5",
    }

    # Resolver nombre del indicador
    nombre_indicador = indicadores.get(indicador_seleccionado, "")

    # Filtrado de atención individual
    atencion_qs = AtencionPoblacion345.objects.all()
    if indicador_seleccionado in indicador_a_edad:
        grupo_edad = indicador_a_edad[indicador_seleccionado]
        atencion_qs = atencion_qs.filter(grupo_de_edad=grupo_edad)

    if ciclo_seleccionado:
        try:
            ciclo_int = int(ciclo_seleccionado)
            atencion_qs = atencion_qs.filter(ciclo_escolar_inicio__inicio=ciclo_int)
        except ValueError:
            pass

    atencion_345__existentes = list(atencion_qs)
    # TODO: Revisar porque no se estan enviando graficos
    # Filtrando gráficos de marginación por localidad
    graficos_marginacion_existentes = MarginacionPoblacion345.objects.all()
    if indicador_seleccionado:
        graficos_marginacion_existentes = graficos_marginacion_existentes.filter(indicador=indicador_seleccionado)
    if ciclo_seleccionado:
        graficos_marginacion_existentes = graficos_marginacion_existentes.filter(ciclo_escolar_inicio_id=ciclo_int)

    # Filtrado de gráficos múltiples según el indicador seleccionado
    graficos_multiples_existentes = graficos_multiples.objects.all()
    if indicador_seleccionado:
        graficos_multiples_existentes = graficos_multiples_existentes.filter(indicador=indicador_seleccionado)



    # Filtrado de definicion de indicadores segun el indicador seleccioando
    definiciones_existentes = IndicadorDefinicion.objects.all()
    if indicador_seleccionado:
        definiciones_existentes = definiciones_existentes.filter(indicador = indicador_seleccionado)

    # Filtrado de interpretación de indicadores segun el indicador seleccionado
    interpretaciones_existentes = interpretaciones_indicadores.objects.all()
    if indicador_seleccionado:
        interpretaciones_existentes = interpretaciones_existentes.filter(indicador = indicador_seleccionado)

    algoritmos_existentes = algoritmos_indicadores.objects.all()
    if indicador_seleccionado:
        algoritmos_existentes = algoritmos_existentes.filter(indicador = indicador_seleccionado)

    contexto = {
        'atencion_345__existentes': atencion_345__existentes,
        'graficos_marginacion_existentes': graficos_marginacion_existentes,
        'ciclos_escolares': ciclos_escolares,
        'indicadores': indicadores,
        'indicador_seleccionado': indicador_seleccionado,
        'nombre_indicador': nombre_indicador,
        'ciclo_seleccionado': ciclo_seleccionado,
        'graficos_multiples_existentes': graficos_multiples_existentes,
        'definiciones_existentes': definiciones_existentes,
        'interpretaciones_existentes': interpretaciones_existentes,
        'algoritmos_existentes': algoritmos_existentes,
    }

    return render(request, 'inicio.html', contexto)
