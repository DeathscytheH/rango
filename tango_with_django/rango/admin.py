#admin.py

from django.contrib import admin
from rango.models import Category, Page, UserProfile

#Modificar el Admin
class PageAdmin(admin.ModelAdmin):
    """docstring for PageAdmin"""
    list_display = ('title', 'category', 'url')

admin.site.register(Category)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)