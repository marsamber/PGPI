from datetime import date
from django import template
register = template.Library()

@register.simple_tag
def setvar(val=None):
  return val

@register.simple_tag
def update_variable(value):
    """Allows to update existing variable in template"""
    return value

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(name='is_future_due')
def is_future_due(self):
    return date.today() <= self