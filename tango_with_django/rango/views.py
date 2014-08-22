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
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    #Request the context of the request.
    #The context contains information such as the client machine details.
    context = RequestContext(request)

    #Contruct dictionary to pass to the template engine as its context
    #The key boldmessage is the same as in the template
    context_dict = {'boldmessage':"I am bold font form the context"}

    #Return a rendered response to send to the client.
    #We make use of the shortcut function to make our lives easier.
    #Note the first parameter is the template we wish to use.
    return render_to_response('rango/index.html', context_dict, context)

def indexSencillo(request):
    return HttpResponse("Rango dice: 'Hola Mundo!' <a href='/rango/about'>About</a>")

def about(request):
    return HttpResponse(" Rango dice: 'Esta es la pagina de acerca de nosotros' <a href='/rango/' class="">Index</a>")