from atexit import register
from django import template
from post.models import *

# cобственные шаблонные теги

register = template.Library()

@register.simple_tag()
def get_car():
    return Car.objects.all()