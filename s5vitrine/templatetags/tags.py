# -*- coding: utf-8 -*-
from django import template
from django.core.paginator import Page
from s5vitrine.models import Menuitem

register = template.Library()


@register.inclusion_tag('s5vitrine/partials/tag.menu.html')
def menu(menu_actif):
    """
    Tag permettant de generer le menu principal de la partie vitrine
    :type menu_actif: Menuitem
    :param menu_actif: Si match avec un autre Menuitem, alors celui-ci est differencie par la
    classe "active"
    """
    menuitems = Menuitem.objects.filter(actif=1).order_by('position',)
    return {
        'menuitems': menuitems,
        'menu_actif': menu_actif
    }


@register.inclusion_tag('s5vitrine/partials/tag.auth_widget.html')
def auth_widget(request):
    username = None
    authenticated = False

    if request.user.is_authenticated():
        username = request.user.username
        authenticated = True

    app_name = request.resolver_match.app_name

    return {
        'username': username,
        'authenticated': authenticated,
        'app_name': app_name
    }


@register.inclusion_tag('s5vitrine/partials/tag.pagination.html')
def pagination(current_page):
    if not isinstance(current_page, Page):
        raise ValueError("Pagination: le paramètre current_page doit être une instance de Page, %s obtenu" % current_page.__class__)

    return {
        'current_page': current_page
    }