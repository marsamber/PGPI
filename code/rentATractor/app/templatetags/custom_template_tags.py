from datetime import date, timedelta
from django import template
register = template.Library()

@register.simple_tag
def setvar(val=None):
  return val

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(name='multiply')
def multipy(value, arg):
    return value * arg

@register.filter(name='addOneWeek')
def addOneWeek(self):
    return self + timedelta(days=7)