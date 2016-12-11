# -*- coding: utf-8 -*-
from django import template
from django.contrib.auth.decorators import login_required

register = template.Library()


@login_required()
@register.inclusion_tag('s5appadherant/partials/tag.menu_adherant.html')
def menu_adherant(user, menu_actif=None):

    if not user.first_name or not user.last_name:
        username = 'Accueil'
    else:
        username = u'%s %s' % (user.first_name, user.last_name)

    return {
        'username': username,
        'menu_actif': menu_actif
    }
