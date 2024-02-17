from django import template

register = template.Library()

@register.filter(name="multiplication")
def multiplication(value1, value2):
    result = value1 * value2
    return result