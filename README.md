# Rango

#### Mi app resultado del tutorial Tango with Django

### Basic Workflow 

#####Chapter 3

- Crear un nuevo proyecto Django
    + Para crear un nuevo proyecto se corre el comando ```django-admin.py startproyect <nombre>``` donde ```<nombre>``` es el nombre del proyecto a crear.
- Crear una nueva aplicacion de Django
    + Para crear una nueva app el comando es ```python manage.py startapp <nombreApp>``` donde ```<nombreApp>``` es el nombre de la app a crear.
    + Agregar la nueva app al proyecto en la tupla de ```INSTALLED_APPS``` en el archivo ```settings.py```.
    + Mapea la aplicacion en el archivo urls.py
    + En la carpeta de la app, crea un archivo ```urls.py``` para direccionar las URL a las vistas.
    + En el archivo ```view.py``` de la app, crear las vistas requeridas. Asegurandonos que regresen un objeto HttpResponse.

##### Chapter 4

- Crear un template e interactuar con el
    + Crear un template y guardarlo en el directorio ```templates``` que especificaste en ```settings.py```. Utiliza variables de django template ({{variable}}). Estas se cambiaran con lo que tu hayas programado en la vista.
    + Encuentra o crea una nueva vista dentro del archivo ```views.py```.
    + Agrega logica a la vista. Por ejemplo, datos de una db.
    + Dentro de la vista, construye un diccionario en el cual puedas pasar al template como parte del ```context```
    + Usa la clase ```RequestContext()``` y la funcion ```render_to_response()``` para generar una respuesta renderisada. Asegurate de referenciar el template correcto para el primer parametro de ```render_to_response()```.
    + No olvidar mapear la vista a una URL en el archivo ```urls.py``` ya sea del proyecto o de la aplicación, si es que lo tienes.
- Agregar archivos estaticos a la pagina.
    + Guarda el archivo estatico que quieras dentro del folder ```static```. Este es el folder que especificas en la tupla ```STATICFILES_DIRS``` dentro de ```settings.py```.
    + Agrega una referencia del archivo en el template. Recuerda utilizar ```{% load static%}``` y ```{% static "nombre" %} dentro del template para ayudarte.
    + Carga la vista que usa el template que modificaste. El archivo debe de aparecer.

##### Chapter 5

- Establecer la DB
    + Escoger cual DB se va a utilizar (configurar ```DATABASES``` en ```setings.py```). Sin esto, Django no sabra donde guardar los datos. Tambien, puedes habilitar la interfaz de admin. Recuerda deshabilitarla cuanto tu app este en producción.
- Agregando un modelo
    + Crea un modelo(s) en ```models.py``` en tu app. 
    + Con el modelo creado, reconfigura la interfaz de admin para incluir tu(s) nuevo(s) modelo(s). Si es que los utilizas.
    + Sincroniza o resincroniza la DB con el comando ```python manage.py syncdb```. Esto creara la infraestructura necesaria dentro de la DB para tu nuevo modelo.
    + Crea/edita y ejecuta un scrip de populado para tu(s) nuevo(s) modelo(s).
    + Recuerda las limitantes de ```syncdb``` para eso utilizaremos ```south```

##### Chapter 6

- Crear una pagina basada en data
    + Importar los modelos en el archivo ```views.py```.
    + Dentro de la vista que vas a usar, hacerle querys al modelo para obtener los datos a presentar.
    + Pasa los resultados del modelo al contexto del template.
    + Prepara el template para mostrar los datos.
    + Mapea la URL a la vista.

##### Chapter 7

- Crear una forma y dejar que los usuarios ingresen datos.
    + Crea un archivo ```forms.py``` dentro del folder de tu app. Ahi se guardaran las clases relacionadas a las formas.
    + Crea una clase ```ModelForm``` por cada modelo que desees representar como una forma.
    + Customizar las formas al gusto.
    + Crear o actualizar una vista para manejar la forma, _incluyendo mostrar la forma, guardando los datos de la forma y mostrando errores que puedan ocurrir cuando el usuario meta datos erroneos o vacios en la forma_.
    + Crear o actualizar un template para mostrar la forma.
    + Agregar un ```urlpattern``` para mapear la nueva vista, si se creo una nueva.