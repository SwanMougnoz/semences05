from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from s5vitrine.models import page, menuitem
from s5appadherant.models import variete


class PageContenuAdminForm(forms.ModelForm):
    contenu = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = page.PageContenu
        fields = ('titre', 'contenu')


class PageContenuAdmin(admin.ModelAdmin):
    form = PageContenuAdminForm


class MenuitemAdminForm(forms.ModelForm):

    class Meta:
        model = menuitem.Menuitem
        exclude = ['_page_generique']


class MenuitemAdmin(admin.ModelAdmin):
    form = MenuitemAdminForm


admin.site.register(page.PageContenu, PageContenuAdmin)
admin.site.register(page.PageGenerique)
admin.site.register(menuitem.Menuitem, MenuitemAdmin)
admin.site.register(variete.Variete)
