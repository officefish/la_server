# -- coding: utf-8 --
from django import template
register = template.Library()


RARITY = {
    '0': 'обычная',
    '1': 'редкая',
    '2': 'эпическая',
    '3': 'легендарная'
}


@register.filter
def rarity(value, arg):
    response = arg

    try:
        response = RARITY[str(arg)]
    except:
        pass

    return response
