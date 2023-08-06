# -*- coding: utf-8  -*-
import datetime

from django import template
from django.utils.html import mark_safe

from ..sites import site

register = template.Library()


@register.inclusion_tag('gas/tags/navigation.html')
def show_navigation(user):
    user_roles = set(user.user_roles.values_list('role', flat=True))
    if user.is_superuser:
        user_roles.add('admins')
    menu = site.get_root_menu(user_roles)
    menu.sort()
    return {
        'menu': menu,
        'user_roles': user_roles,
    }


@register.filter
def get_children(entry, roles):
    return sorted(
        [
            child for child in entry.children.values()
            if child.roles.intersection(roles)
        ],
    )


@register.filter()
def display_boolean(value):
    if bool(value):
        render = '<i class="fas fa-check"></i>'
    else:
        render = '<i class="fas fa-times"></i>'
    return mark_safe(render)
