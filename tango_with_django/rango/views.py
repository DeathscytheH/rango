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
from rango.models import Category, Page

def category(request, category_name_url):
    context = RequestContext(request)

    #Cambiamos espacios en blanco por '_'
    category_name = category_name_url.replace('_',' ')

    #Diccionario con el nombre de la categoria
    context_dict = {'category_name': category_name}

    try:
        #Existe la categoria que buscamos?
        #Si no, el metodo .get() lanza una excepcion DoesNotExist
        #El metodo .get() o regresa una instancia del modelo o lanza una excepcion.
        category = Category.objects.get(name = category_name)

        #Obtener todas las paginas asociadas
        #Los filtros regresan >= 1 de las instancias del modelo
        pages = Page.objects.filter(category = category)

        #Agregan la lista de resultados al template
        context_dict['pages'] = pages

        #Agregamos el objeto categoria de la DB al diccionario
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render_to_response('rango/category.html', context_dict, context)

def index(request):
    context = RequestContext(request)

    #Query la db por una lista de todas las categorias guardadas
    #Ordenan por el numero de likes de mayor a menor
    #Solo el top 5 o todas si son menores a 5
    category_list = Category.objects.order_by('-likes')[:5]

    #Se guarda en el diccionario
    context_dict = {'categories': category_list}

    #Ciclamos por cada categoria y creamos un atributo URL
    #Este atributo guarda la URL codificada
    for category in category_list:
        category.url = category.name.replace(' ', '_')

    #Lo renderisamos
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)
    context_dict = {'mensaje':'ola ke ase!!!'}
    return render_to_response('rango/about.html', context_dict, context)

"""
def indexMedio(request):
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

def aboutSencillo(request):
    return HttpResponse(" Rango dice: 'Esta es la pagina de acerca de nosotros' <a href='/rango/' class="">Index</a>")
    """