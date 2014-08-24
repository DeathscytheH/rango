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
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#Para desloguearse requiere estar logueado
@login_required
def user_logout(request):
    #El usuario esta logueamo, solo lo deslogueamos
    logout(request)

    #Lo redireccionamos al home
    return HttpResponseRedirect('/rango/')

@login_required
def restricted(request):
    return HttpResponse('Lo puedes ver porque estas logueado.')

def user_login(request):
    context = RequestContext(request)

    #Si es un POST jalamos los datos
    if request.method=='POST':
        #Juntamos el username y pass que nos da el usuario
        #Esta info es obtenida de la forma login
        username = request.POST['username']
        password = request.POST['password']

        #Utilizamos los metodos de django para saber si las credenciales son validas
        #Si si lo son, nos regresa un objeto User
        user = authenticate(username = username, password= password)

        #Si tenemos un objeto User, las credenciales son correctas.
        #Si obtenemos un None, el usuario no esta registrado.
        if user:
            #La cuenta esta activa?
            if user.is_active:
                #Si la cuenta es valida y activa, podemos loguear al usuario.
                #Y mandarlo a home
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                #Encontramos una cuenta deshabilitada
                return HttpResponse('Tu cuenta esta deshabilitada')
        else:
            #Credenciales no validas
            print 'Login invalido: {0}, {1}'.format(username, password)
            return HttpResponse('Login invalido. Revisa tu password y/o usuario')
    #La peticion no es POST asi que mostramos la forma de login
    else:
        #No se van a pasar variables al template, por lo tanto el diccionario va vacio.
        return render_to_response('rango/login.html', {}, context)


def register(request):
    context = RequestContext(request)

    #Un valor boleano que le dice al template si el registro fue exitoso.
    #inicialmente falso. Se cambiara mas adelante.
    registered=False

    #Si es un HTTP POST, procesaremos los datos.
    if request.method == 'POST':
        #Intentamos obtener la informacion de la forma
        #Utilizamos ambas formas UserForm y UserProfileForm
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #Si las dos formas son validas
        if user_form.is_valid() and profile_form.is_valid():
            #Guardamos los datos de la forma en la DB
            user = user_form.save()

            #Se hashea el pass con el metodo set_password
            #Una vez hasheado, actualizamos el objeto usuario
            user.set_password(user.password)
            user.save()

            #Ahora sobre la instancia de UserProfile
            #Los atributos del modelo user los tenemos que poner nosotros, ponemos commit = false
            #Con esto detenemos el guardar en la DB, hasta que estemos seguros de que no hay errores
            profile = profile_form.save(commit=False)
            profile.user = user

            #El usuario eligio una imagen?
            #Si si lo hizo, hay que obtenerla de la forma y ponerla en el modelo UserProfile
            if 'picture' in request.FILES:
                profile.picture=request.FILES['picture']

            #Ahora salvamos la instancia del modelo UserProfile
            profile.save()

            #Actualizamos la variable para decirle al template que el registro fue exitoso
            registered=True
        #Forma o formas invalidas - errores o algo
        #Imprime en terminal los errores.
        #Tambien se mostraran al usuario.
        else:
            print user_form.errors, profile_form.errors
    #No es un HTTP POST, asi que las dos instancias de ModelForm se renderizaran.
    #Estas formas estaran en blanco, listas para el usuario.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    #Renderizamos el template dependiendo del contexto
    return render_to_response('rango/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered}, context)

@login_required
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

@login_required
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