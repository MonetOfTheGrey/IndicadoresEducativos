from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

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
    return render(request, 'blank.html')