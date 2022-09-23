
from multiprocessing import AuthenticationError
from xml.dom import ValidationErr
from django import forms
from matplotlib import widgets
from .models import *
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget,AdminSplitDateTime
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
import re
from captcha.fields import CaptchaField



class Callback_Form(forms.ModelForm):
    #сделать поле не обязательным - комментарии
    #validation name
    captcha = CaptchaField( )   #проверка на бота
    class Meta():
        model = Callback    #связь с моделью в model
        #fields = "__all__"  # все поля наследуем кроме тех которые заполняются автоматически
        fields = ['name','number','comment_order'] #поля для отображения на странице
        widgets = {
            #'name': forms.TextInput(attrs={'class':'form-input'} on style css
            'comment_order': forms.Textarea(attrs={'cols':16,'rows':2})
        } #для какого поля будем определять тот или иной стиль
    
    def clean_name(self):#clean_ 'name'(is pole validation)
        #имя должно содержать буквы английского или русского алфавита
        #
        name = self.cleaned_data['name']
        if not name.isalpha():#состоит ли строка только из буквенных символов
            #требуется добавить если будет состоять из двух слов через пробел
            raise ValidationError("Имя должно состоять из букв")
        return name

    def clean_number(self):  
        number = self.cleaned_data['number']
        if len(number)<11:
            raise ValidationError('Номер телефона короче 11 символов')
        else:
            numbers = re.match(r"(\+7|7|8)(\d[0-9]{9})", number)
            if not numbers:
                raise ValidationError("Номер телефона не валиден.Пример номера 8921755....")
            return number  
        
    
class To_come_in(forms.Form): 
    login = forms.CharField(max_length=15, label= 'логин',required=False)
    password = forms.CharField(max_length=10, label= 'пароль',required=False)
    save_password = forms.BooleanField(label= 'запомнить',required=False, initial=True )


class Registration_Form(UserCreationForm): # добавить номер телефона и имя
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    email = forms.EmailField(label = 'Почта', widget = forms.EmailInput())
    password1 = forms.CharField(label = 'Пароль', widget= forms.PasswordInput())
    password2 = forms.CharField(label = 'Повтор пароля', widget= forms.PasswordInput())
    captcha = CaptchaField()

    class Meta():
        model = User
        fields = ['username','email','password1','password2']  #nomber phone,'first_name' - need to past
     

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',widget=forms.TextInput()) 
     #widget=forms.TextInput(attrs{'class': 'form-input'}) оформление поля через стили css
    password = forms.CharField(label="Пароль", widget=forms.TextInput())

class Online_orderForm(forms.ModelForm): #эта модель подключена к странице order_taxi для формы заказа.Пока все поля обязательные
    #time_order = forms.TimeField(widget=AdminTimeWidget()) #подсказчик выбора
    class Meta:

        model = Online_order    #наследование класса
        #fields = "__all__"  # все поля наследуем кроме тех которые заполняются автоматически
        fields = ['first_name','phone','a','b','date','time_order','cars','comment_driver','baby_chair','smoking','music']
        widgets = {     #подключить образец заполнения даты и времени 
            'time_order': AdminTimeWidget(), # work
            'date': AdminDateWidget(),
        }
    def __init__(self,*args,**kwargs):#konstructor
        super(Online_orderForm,self).__init__(*args,**kwargs)
        self.fields['cars'].empty_label = 'Автомобиль не выбран'
        #self.fields['time_order'].widget = widgets.AdminTimeWidget() # work
        #self.fields['date'].widget = widgets.AdminDateWidget()    
        
    def clean_first_name(self):#clean_ 'name'(is pole validation)
        #имя должно содержать буквы английского или русского алфавита
        #
        name = self.cleaned_data['first_name']
        if not name.isalpha():#состоит ли строка только из буквенных символов
            #требуется добавить если будет состоять из двух слов через пробел
            raise ValidationError("Имя должно состоять из букв")
        return name

    def clean_phone(self): #validation nomber
        #проверка номера телефона через регулярное выражение
        # re.match(r'\+7|7|8)\d[0-9]{9}') - регялярное выражение для валидации номера телефона    
        phone = self.cleaned_data['phone']
        if len(phone)<11:
            raise ValidationError('Номер телефона короче 11 символов')
        else:
            number = re.match(r"(\+7|7|8)(\d[0-9]{9})", phone)
            #print(number)
            if not number:
                raise ValidationError("Номер телефона не валиден или начинается не с 8...")
            return phone    
        