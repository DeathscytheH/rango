from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    """docstring for Category"""    
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class Page(models.Model):
    """docstring for Page"""
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    #La siguiente linea es de ley. Liga UserProfile con una instancia del modelo User
    user = models.OneToOneField(User)

    #Los atributos extras que queremos incluir.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    #Sobreescribimos el metodo unicode para obtener algo significativo.
    def __unicode__(self):
        return self.user.username