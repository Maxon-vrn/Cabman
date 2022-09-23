from multiprocessing import AuthenticationError
from urllib import request
from django.views.generic import ListView,CreateView
from django.views.generic import View
from re import template
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout

from .models import*    #подключаем базу данных
from .forms import *
from .utils import *

menu = ['Главная страница','Наши услуги','Автопарк','О нас','Контакты']


class PostHome(View): #View - базовый класс представлений от него наследуются все остальные
    template_name = 'taxi/index.html'

    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_contex_data(**kwargs)
    
        return context

    def get(self, request, *args, **kwargs):
        return render(request, 'taxi/index.html')


class Garage(ListView): #in listview есть пагинатор для отображения страниц
    paginate_by = 4 #количество постов на одной странице
    model = Car     #обязательно наличие модели для данного представления!
    template_name = 'taxi/garage.html'   #подсказывает путь к шаблону
    context_object_name = 'posts'   #переменная используемая в шаблоне при работе с бд


    def get_queryset(self): #
        return Car.objects.filter(is_published = True) #возвращает только опубликованные в админке записи на страницу
#def garage(request):
#    cars = Car.objects.all() #выбираем все объекты с базы данных
#    return render(request, 'taxi/garage.html', {'posts': cars,'menu':menu, 'title':'Автопарк'})


def service(request):
    return render(request, 'taxi/service.html') 


class Employees(LoginRequiredMixin,ListView):   #looginmixim - отрабатывает доступ к странице зарегистрированных лиц
    model = Driver     #обязательно наличие модели для данного представления!
    template_name = 'taxi/about.html'   #подсказывает путь к шаблону
    context_object_name = 'drivers'   #переменная используемая в шаблоне при работе с бд
    login_url = reverse_lazy('about_no_autorization')  #переадресация для неавторизованных пользователей на другую страницу
    #raise_exception = True #выдача ошибки 403 при доступен на старницу, используется вместо веше строки 
    
    
    def get_queryset(self): #
        return Driver.objects.filter(is_published = True) #возвращает только опубликованные в админке записи на страницу

    #def about(request):
    #    drivers = Driver.objects.all() #выбираем все объекты с базы данных
    #    person = Driver.objects.filter(first_name = 'Max')
    #    return render(request, 'taxi/about.html', {'drivers': drivers, 'menu':menu, 'person': person}) 

def  about_no_autorization(request):
    return render(request, 'taxi/about_no_autorization.html')


#@login_required - декоратор доступа только для зарегистрированныйх пользователей
def contact(request):
    return render(request, 'taxi/contact.html') 


class LoginUser(LoginView):
    form_class = LoginUserForm  #Используем свою форму для иутентификации а сайте
    #Django standart form to user authentification form_class = AuthenticationForm
    template_name = 'taxi/to_come_in.html'

    def get_success_url(self):
        return reverse_lazy('home')


""" def to_come_in(request): #страница входа / регистрации
    if request.method == "POST":
        form = To_come_in(request.POST)
        if form.is_valid(): #проверка корректности введеных данных
            print(form.cleaned_data)
            return redirect('home')
            #try:
                #Client_Registration.objects.create(**form.cleaned_data)
                #return redirect('home')
            #except:
                #form.add_error(None, 'ошибка добавления')        
    else:
        form = To_come_in()
    return render(request, 'taxi/to_come_in.html', {'form':form})   """


def logout_user(request):
    logout(request) #standart django method 
    return redirect('to_come_in')
    
     
class RegisterUser(CreateView): #ругается на неопределенную базу данных
    form_class = Registration_Form   #Django standart form to registration
    template_name = 'taxi/registration.html'    #ссылка на страницу
    success_url = reverse_lazy('to_come_in') #переадресация в случае удачной отправки

    def form_valid(self,form):  #если пользователь ввел корректно все поля  то вызывается этот метод
        user = form.save()
        login(self.request,user)    #automatic avtorisation on sait
        return redirect('home')
    #def get_context_data(self,*,object_list=None, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    c_def = self.get_user_context(title = 'Регистрация')
     #   return dict(list(context.items())+list(c_def.items()))  #dict(list(context.items())))
    

""" def registration(request):
    if request.method == "POST":
        form = Registration_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('to_come_in')   #redirect work
        else:
            print("Error", form.errors)    
    else:
        form = Registration_Form()
    return render(request, 'taxi/registration.html', {'form':form}) """


def order_taxi(request):
    print(request) #просмотр данных отправляемы в базу данных и ошибки
    if request.method == "POST":
        form = Online_orderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order')
        else:
            print("Error", form.errors)
    
    else:
        form = Online_orderForm() #после отправки формы заполненной,после отправки страница новая с чистыми формами
    return render(request, 'taxi/order_taxi.html', {'form':form})    


def order(request): #redirect - work,but not name client in form
    #name = request.POST['name']
    return render(request, 'taxi/order.html')    


def callback(request):    #страница для обратного звонка
    print(request)
    if request.method == "POST":
        form = Callback_Form(request.POST)
        if form.is_valid():
            form.save() #it's work
            return redirect('callback_order') # work
        else:
            print("Error", form.errors)    
    else:
        form = Callback_Form() #подключение формы к старнице
    return render(request, 'taxi/callback.html', {'form':form})   


def callback_order(request): #настроить редирект на эту страницу GET or POST с именем из функции callback
    if request.method == "POST":
        print(request)
        pass
    elif request.method == "GET":
        print(request)
        for key,value in request.GET.items():
            print(key,'->',value)
        #name = request.GET['name']
    # re"^(\+7|7|8)\d[0-9]{9}" - регялярное выражение для валидации номера телефона    
    return render(request, 'taxi/callback_order.html') #redirect to start page on html




def pageNotFound(request,exeption): #обработка исключений при ненахождении старниц/запроса
    return HttpResponseNotFound('<h1> Страница не найдена и обработана успешно функцией </h1>')

#def pageNotFound1(request,exeption): #обработка исключений при ненахождении старниц/запроса #500
    return HttpResponseNotFound('<h1> Страница не найдена и обработана успешно функцией </h1>')   