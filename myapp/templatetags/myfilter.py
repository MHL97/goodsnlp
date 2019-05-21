# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter
def key(dict_name, key_name):
    value = 0
    try:
        value = dict_name[key_name]
    except KeyError:
        value = 0
    return value