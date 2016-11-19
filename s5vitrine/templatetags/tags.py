from django import template
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


@register.inclusion_tag('s5vitrine/partials/tag.login_toggler.html')
def login_toggler(request):
    username = None
    authenticated = False

    if request.user.is_authenticated():
        username = request.user.username
        authenticated = True

    return {
        'username': username,
        'authenticated': authenticated
    }

