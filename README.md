# Rango

### Mi app resultado del tutorial Tango with Django

#### Basic Workflow

- Crear un nuevo proyecto Django
    + Para crear un nuevo proyecto se corre el comando ```django-admin.py startproyect <nombre>``` donde ```<nombre>``` es el nombre del proyecto a crear.
- Crear una nueva aplicacion de Django
    + Para crear una nueva app el comando es ```python manage.py startapp <nombreApp>``` donde ```<nombreApp>``` es el nombre de la app a crear.
    + Agregar la nueva app al proyecto en la tupla de ```INSTALLED_APPS``` en el archivo ```settings.py```.
    + Mapea la aplicacion en el archivo urls.py
    + En la carpeta de la app, crea un archivo ```urls.py``` para direccionar las URL a las vistas.
    + En el archivo ```view.py``` de la app, crear las vistas requeridas. Asegurandonos que regresen un objeto HttpResponse.