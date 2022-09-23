# адреса которые будут обрабатывать наше приложение с которыми он будет работать
# написано для переносимости ресурса

from django.urls import path,re_path
from .views import *
from django.views.generic import TemplateView #ллассы представлений
from django.views.i18n import JavaScriptCatalog #для подключение AdminDateTime
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', PostHome.as_view(), name='home'),    # 127.0.0.1:8000
    #path('', cache_page(60)(PostHome.as_view()), name='home'), #cache_page(60-time)(what we put inside)
    # кеширование страниц подключаем в самую последнюю очередь чтобы избежать скрытия sql запросов при отладке
    path('jsi18n',JavaScriptCatalog.as_view, name= 'js-catlog'),    #попытка подключить время и дату помошника на сайте
    path('order_taxi/', order_taxi, name='order_taxi'),
    path('order/', order , name='order'),
    path('callback/',callback, name='callback'),
    path('callback_order/', callback_order, name='callback_order'),
    path('service/', service, name = 'service'),
    path('garage/', Garage.as_view(), name = 'garage'),    # 127.0.0.1/garage/
    # int,str,slug -латиница и таблицы символы дефиса и подчеркивания,uuid -цифры и малые латинские символы дефисы,path - любая не пустая строка
    path('about/', Employees.as_view() , name ='about'),
    path('about_no_autorization/',about_no_autorization, name = 'about_no_autorization'),
    path('contact/', contact , name ='contact'),
    path('to_come_in/', LoginUser.as_view(), name ='to_come_in'),
    path('registration/', RegisterUser.as_view(), name ='registration'),
    path('logout/', logout_user , name ='logout'),
    #re_path(r"^archive/(?P<year>[0-9]{4})/",archive), #регулярное выражение
    
]
