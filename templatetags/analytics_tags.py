from django import template

register = template.Library()

@register.filter
def divisor(value, arg):
    """Divide the value by the argument if arg is not 0"""
    try:
        if int(arg) != 0:
            return float(value) / float(arg)
        return 0
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0