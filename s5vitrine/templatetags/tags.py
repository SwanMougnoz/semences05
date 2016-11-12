from django import template
from s5vitrine.models import Menuitem

register = template.Library()


@register.inclusion_tag('s5vitrine/partials/tag.menu.html')
def menu(menu_active):
    menuitems = Menuitem.objects.all().order_by('position',)
    return {
        'menuitems': menuitems,
        'menu_active': menu_active
    }
