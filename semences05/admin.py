from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from s5vitrine.models import page, menuitem
from s5appadherant.models import variete


class PageContenuAdminForm(forms.ModelForm):
    contenu = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = page.PageContenu
        fields = ('titre_page', 'titre', 'contenu')


class PageContenuAdmin(admin.ModelAdmin):
    form = PageContenuAdminForm


admin.site.register(page.PageContenu, PageContenuAdmin)
admin.site.register(page.PageGenerique)
admin.site.register(menuitem.Menuitem)
admin.site.register(variete.Variete)
