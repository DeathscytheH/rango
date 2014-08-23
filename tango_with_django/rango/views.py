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
from rango.forms import CategoryForm, PageForm

def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decodeUrl(category_name_url)

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            #No podemos hacer commit inmediatamente
            #No todos los campos se populan automaticamente.
            page=form.save(commit=False)

            #Obtenemos el objeto categoria asociado para agregarlo
            #Usamos un try. Checamos que la categoria exista.
            try:
                cat=Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                #La categoria no existe.
                #Renderizamos la forma de agregar categorias por mientras.
                return render_to_response('rango/add_category.html', {}, context)

            #Creamos un valor default para el numero de vistas
            page.views = 0

            #Salvamos la instancia del nuevo modelo
            page.save()

            #Ya la pagina salvada mostramos la categoria
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response('rango/add_page.html',{'category_name_url':category_name_url, 'category_name': category_name, 'form':form}, context)

def add_category(request):
    context = RequestContext(request)

    #A HTTP POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        #Es una forma valida?
        if form.is_valid():
            #Guardamos los datos
            form.save(commit=True)

            #Le hablamos a la vista index()
            #Regresamos al usuario al home
            return index(request)
        else:
            #La forma tiene errores, los mostramos
            print form.errors
    else:
        #Si no es un post, mostrar la forma para ingresar datos.
        form=CategoryForm()

    #Una forma erronea o vacia
    #Se renderiza la forma con los mensajes de error, si hay.
    return render_to_response('rango/add_category.html', {'form': form}, context)

def category(request, category_name_url):
    context = RequestContext(request)

    #Cambiamos espacios en blanco por '_'
    category_name = decodeUrl(category_name_url)

    #Diccionario con el nombre de la categoria
    context_dict = {'category_name': category_name, 'category_name_url': category_name_url}

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
    page_list = Page.objects.order_by('-views')[:5]

    #Se guarda en el diccionario
    context_dict = {'categories': category_list, 'pages': page_list}

    #Ciclamos por cada categoria y creamos un atributo URL
    #Este atributo guarda la URL codificada
    for category in category_list:
        category.url = encodeUrl(category.name)

    #Lo renderisamos
    return render_to_response('rango/index.html', context_dict, context)

def encodeUrl(str):
    return str.replace(' ', '_')

def decodeUrl(str):
    return str.replace('_', ' ')

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