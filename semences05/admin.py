from django.contrib import admin
from s5vitrine.models import page, menuitem

admin.site.register(page.PageContenu)
admin.site.register(page.PageGenerique)
admin.site.register(menuitem.Menuitem)
