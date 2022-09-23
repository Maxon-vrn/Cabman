from multiprocessing.connection import Client
from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

# Register your models here.
# говорит о том как отображаться в админ панели вашему приложению

class CarAdmin(admin.ModelAdmin):
    list_display= ('id','title','year_avto','time_create','distance','get_html_photo','is_published')
    list_display_links = ('id','title') #поля на которые мы можем кликнут  и перейти
    search_fields = ('title','content') #по каким поля м можно искать информацию
    list_editable= ('is_published',) #возможноть снимать с публикации рчерез админку тот или иной автомобиль
    list_filter = ('is_published','time_create') #настройка фильтрации по полям

    def get_html_photo(self,object):    #отображение миниатюры фотографии авто в админ панели
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50>')
    get_html_photo.short_description = 'Миниатюра'

class DriverAdmin(admin.ModelAdmin):
    list_display= ('id','first_name','last_name','date_birth','get_html_photo1','cars','language_person','is_published')
    list_display_links=('id','first_name','last_name','get_html_photo1','cars')
    list_editable = ['is_published',]
    search_fields = ('id','first_name','last_name','date_birth','cars','language_person')

    def get_html_photo1(self,object):    #отображение миниатюры фотографии авто в админ панели
        if object.photo_person:
            return mark_safe(f'<img src="{object.photo_person.url}" width=50>')
    get_html_photo1.short_description = 'Миниатюра'


class Online_orderAdmin(admin.ModelAdmin):
    list_display=('first_name','phone','comment_driver','a','b','time_order','time_create','cars','baby_chair','smoking','music')
    search_fields = ('first_name','phone','comment_driver','a','b','time_order','time_create','cars')
    list_display_links= ('first_name','phone','comment_driver','a','b','time_order','time_create')
    list_filter = ('first_name','phone','comment_driver','a','b','time_order','time_create','cars')

class Callback_Admin(admin.ModelAdmin):

    list_display = ('name','number','comment_order','time_create','is_published')
    list_display_links = ('name','number')
    search_fields = ('name','number','comment_order','is_published')
    list_filter = ('is_published',)
    

admin.site.register(Car, CarAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Online_order,Online_orderAdmin)
admin.site.register(Callback,Callback_Admin)