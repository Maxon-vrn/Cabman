from django.apps import AppConfig

# название и конфигурация вашего приложения


class PostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post'
    verbose_name = 'Наполнение сайта'
