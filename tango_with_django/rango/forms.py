#forms.py

from django import forms
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    """docstring for CategoryForm"""
    name = forms.CharField(max_length=128, help_text="Por favor ingresa el nombre de la categoria.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)

    #Una clase que provee info adicional sobre la forma
    class Meta:
        """docstring for Meta"""
        #Una asociacion entre ModelForm y el modelo.
        model = Category

class PageForm(forms.ModelForm):
    """docstring for PageForm"""
    title = forms.CharField(max_length=128, help_text="Por favor ingresa el titulo de la pagina")
    url = forms.CharField(max_length=200, help_text="Por favor ingresa la URL de la pagina")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)

    #Por si el usuario no ingresa bien los datos
    def clean(self):
        cleaned_data=self.cleaned_data
        url= cleaned_data.get('url')

        #Si URL no esta vacia y no inicia con http://, se la pegamos
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url']=url
        
        return cleaned_data

    class Meta:
        model = Page

        #Que campos mostraremos en nuestra forma?
        #De esta manera no mostramos cada campo del modelo
        #Algunos campos del modelo permiten NULL como valor.
        #Con el codigo siguiente no mostramos la llave foranea.
        fields = ('title', 'url', 'views')

class UserForm(forms.ModelForm):
    #El de default, el renderizado sale mal. Hay que especificarlo
    username = forms.CharField(help_text="Por favor ingresa un nombre de usuario.")
    email = forms.CharField(help_text="Por favor ingresa tu correo electronico.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Por favor ingresa un password.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Ingresa tu sitio web.", required=False)
    picture = forms.ImageField(help_text="Selecciona una imagen para tu perfil.", required=False)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

