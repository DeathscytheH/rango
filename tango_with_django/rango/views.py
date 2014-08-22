# Create your views here.

"""
- Primero se importa el objeto HttpResponse del modulo django.http.
- Cada vista existe dentro de view.py como una serie de funciones individuales.
    Aqui solo se creo una vista llamada index
- Cada vista toma un argumento - un objeto HttpRequest, que tambien esta en el 
    modulo django.http. La convencion dicta que que sea llamado request.
- Cada vista debe regresar un objeto HttpResponse. Un objeto simple HttpResponse 
    toma una cadena como parametro, representando el contenido de una pagina
    que deseamos enviar al cliente solicitando la vista.

"""
from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango dice: 'Hola Mundo!' <a href='/rango/about'>About</a>")

def about(request):
    return HttpResponse(" Rango dice: 'Esta es la pagina de acerca de nosotros' <a href='/rango/' class="">Index</a>")