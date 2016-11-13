from django import template
from s5vitrine.models import Menuitem

register = template.Library()


@register.inclusion_tag('s5vitrine/partials/tag.menu.html')
def menu(menu_active):
    """
    Tag permettant de generer le menu principal de la partie vitrine
    :type menu_active: str
    :param menu_active: Si match avec l'identifier d'un Menuitem, alors celui-ci est differencie par la
    classe "active"
    """
    menuitems = Menuitem.objects.all().order_by('position',)
    return {
        'menuitems': menuitems,
        'menu_active': menu_active
    }
