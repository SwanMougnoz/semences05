# -*- coding: utf-8 -*-
from django import template
from django.contrib.auth.decorators import login_required
from context_processors import adherant

register = template.Library()


@login_required()
@register.inclusion_tag('s5appadherant/partials/tag.menu_adherant.html')
def menu_adherant(request, menu_actif=None):

    user = request.user
    if not user.first_name or not user.last_name:
        username = 'Accueil'
    else:
        username = u'%s %s' % (user.first_name, user.last_name)

    context = {'username': username, 'menu_actif': menu_actif}

    # fixme: Comment obtenir cette valeur via le context processor utilisé autre part ?
    context_adherant = adherant(request)
    context.update(context_adherant)
    return context
