from django.contrib import admin
from s5vitrine.models import page, menuitem
from s5appadherant.models import variete

admin.site.register(page.PageContenu)
admin.site.register(page.PageGenerique)
admin.site.register(menuitem.Menuitem)
admin.site.register(variete.Variete)
