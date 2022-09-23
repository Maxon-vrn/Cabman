from audioop import reverse
from distutils.command.upload import upload
from email.policy import default
from tabnanny import verbose
from django.db import models


class Car(models.Model):
    title = models.CharField(max_length=255, verbose_name='Модель',default=' ') #name model avto
    year_avto = models.DateField(null=True,verbose_name='Год производства автомобиля')
    distance = models.CharField(max_length=6,verbose_name='Пробег автомобиля',default=' ')
    content = models.TextField(blank=True, verbose_name='Текст статьи',default=' ') #описание автомобиля и его класса/дополнительных плюшек/TV/game
    photo = models.ImageField(upload_to = "photos/%Y/%m/%d/", verbose_name='Фото',default=' ') #1 общий вид
    photo2 = models.ImageField(upload_to = "photos/%Y/%m/%d/", verbose_name='Фото',default=' ',blank=True) #2 вид с другого ракурса blank=True-необязательное поле
    photo3 = models.ImageField(upload_to = "photos/%Y/%m/%d/", verbose_name='Фото',default=' ',blank=True) #3 салон 
    photo4 = models.ImageField(upload_to = "photos/%Y/%m/%d/", verbose_name='Фото',default=' ',blank=True) #4 плюшки
    photo5 = models.ImageField(upload_to = "photos/%Y/%m/%d/", verbose_name='Фото',default=' ',blank=True) #5 багажник

    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    

    def __str__(self): #Car.objects.all() -> shell :<QuerySet [<Car: Camry>, <Car: Laurel>]>
        # эта конструкция возвращает заготловок текущей записи
        return self.title

    def get_absolute_url(self): #кнопка смотреть на сайте
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta(): #замена имени в админ панели
        verbose_name = 'Cars'    
        verbose_name_plural = 'Автомобили'
        ordering=['title'] #сортировка по значению/полю
 
class Driver(models.Model): 
    """this is model in djanjo -> field types"""
    first_name = models.CharField(max_length=50,verbose_name='Имя',default=' ')
    last_name = models.CharField(max_length=70,verbose_name='Фамилия',default=' ',blank=True)
    date_birth = models.DateField(null=True) #дата рождения убрать время
    photo_person = models.ImageField(upload_to = 'driver/%Y/%m/%d/',verbose_name='Фото водителя',default=' ',blank=True)
    content = models.TextField(blank=True, verbose_name='Описание водителя',default=' ') #описание водителя произвольное
    # нужно связать водителя и автомобиль по id
    cars = models.ForeignKey('Car', on_delete=models.PROTECT) # ключ доступа к другой базе

    education = models.CharField(max_length=100,verbose_name='Образование',default=' ') #образование
    language_person= models.CharField(max_length=50,verbose_name='Знание языков',default=' ') # знание языков у водителя
    driving_experience = models.DateField(null=True,verbose_name='Водительсктий стаж') #date to start drivin car
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.first_name 

    class Meta(): #замена имени в админ панели
        verbose_name = 'Drivers'    
        verbose_name_plural = 'Водители автопарка'  
        ordering=['first_name']  


""" class Client_Registration(models.Model): # логин и пароль и другие данные при регистрации человека на странице
    login = models.CharField(max_length=15,unique=True,verbose_name='Логин',default=' ')
    #unique=True - уникальный |blank=True - необязательное поле 
    first_name = models.CharField(max_length=50,verbose_name='Имя')
    password = models.CharField(max_length=10,verbose_name='Пароль')
    email = models.EmailField(max_length=70,null=True, blank=True, unique=True)
    phone = models.CharField(max_length=12,verbose_name='Номер телефона')
    time_create = models.DateTimeField(auto_now_add=True)
    telegram_user = models.BooleanField() #окно выбора:есть ли твой номер в телеге
    #выпадающий список с выбором да/нет/@ - при выборе  @ подгружается дополнительное окно с графой для ввода логина с телеги

    def __str__(self):
        return self.login #отображение в админке

    class Meta(): #замена имени в админ панели
        verbose_name = 'Client_ registrations'    
        verbose_name_plural = 'Зарегистрированные клиенты'
        ordering=['login'] #сортировка по значению/полю    """

class Online_order(models.Model): #форма для онлайн заказа такси DTModel
    # необходимо свести таблицу заказа с полями в базе данных этого раздела!!!!
    first_name = models.CharField(max_length=30,verbose_name='Введите ваше имя ')
    phone = models.CharField(max_length=12,verbose_name='Ваш номер телефона ')
    a = models.CharField(max_length=100, verbose_name='Куда подать автомобиль ', blank=True) # точка подачи автомобиля и точка конечного придытия
    b = models.CharField(max_length=100,verbose_name='Место назначения ', blank=True)
    date = models.DateField(null=True,verbose_name='Дата подачи автомобиля')
    time_order = models.TimeField(null=True ,verbose_name='Время подачи авто') #время подачи
    comment_driver = models.CharField(max_length=500,verbose_name='Коментарии водителю',blank=True)
    time_create = models.DateTimeField(auto_now_add=True,verbose_name='Время создания') #сегодняшняя дата оформления заказа
    #дополнительные опции выбираемые клиентом
    baby_chair = models.BooleanField(default=False,verbose_name='Детское кресло') #опции для автомобилей (детское кресло и тд)
    smoking = models.BooleanField(default=False,verbose_name='Курение в авто')
    music = models.BooleanField(default=False,verbose_name='Музыка клиента')
    #language = models.BooleanField(default=False,verbose_name='Speek english')
    #helper_today = models.BooleanField(default=False,verbose_name='Личный помощник')
    #при выборе helper_today - заказ должен делаться на целый день
    #dress_code = models.BooleanField(default=False,verbose_name='Дресс код')
    
    cars = models.ForeignKey('Car', on_delete=models.PROTECT,default=' ',verbose_name='Выберите автомобиль') # выбор автомобиля через форму на сайте

    def __str__(self):
        return self.first_name

    class Meta(): #замена имени в админ панели
        verbose_name = 'Online_orders'    
        verbose_name_plural = 'Заказы такси с сайта'
        ordering=['time_create'] #сортировка по значению/полю
        
class Callback(models.Model):
    name = models.CharField(max_length=50,verbose_name='Ваше имя')
    number = models.CharField(max_length=12,verbose_name='Номер для связи') #min11 max12 символов в номеретелефона 
    comment_order = models.CharField(max_length=500,verbose_name='Коментарии',blank=True) 
    time_create = models.DateTimeField(auto_now_add=True) #создание заявки  
    time_change = models.DateTimeField(auto_now= True)  # изменнение/обработка заявки
    is_published = models.BooleanField(default=False, verbose_name='обработанная заявка')
   
    
    def __str__(self):
        return self.name

    class Meta(): #замена имени в админ панели
        verbose_name = 'Callbacks'    
        verbose_name_plural = 'заказы перезвонить с сайта'
        ordering=['time_create'] #сортировка по значению/полю    

class Rewies(): #отзывы клиентов -> index.html page 
    pass    