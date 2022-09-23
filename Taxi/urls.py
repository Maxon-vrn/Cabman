"""Taxi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import imp
from xml.dom.minidom import Document
from django.conf import settings                #для отладки
from django.conf.urls.static import static      #для отладки
from django.contrib import admin
from django.urls import path
from post.views import *  #-импорт всех функций что есть в данnом файле
from post.views import *  #смотри древо импортированных каталогов импорт функции из файла находящегося по адресу
from django.urls import include # - функция представления

def i18n_javascript(request):   # widgets date and time in form to order
      return admin.site.i18n_javascript(request)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    # path('', index) - по запросу в адресной строке 127.0.0.1:8001
    #path('index/', index), # по запросу в адресной строке 127.0.0.1:8001/index/ вернуть все из функции index(из файла views.py)
    #path('garage/', garage), 
    path('',include('post.urls')), # это необходимо для переносимости приложения
    # 1 параметр добавляется при переходе по ссылке 127.0.0.1:8001
    # 2 параметр содержит маршруты к нашим файлам
]
if settings.DEBUG: #в режиме отладки появится путь к загруженным файлам
    import debug_toolbar
    urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound   #функция обработки исключений(когда страница не найдена)
#handler500 = pageNotFound1
