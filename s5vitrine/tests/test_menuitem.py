from django.test import TestCase
from s5vitrine.models import Menuitem, PageGenerique, PageContenu


class MenuitemTest(TestCase):

    fixtures = ['base']

    def test_page_propertie(self):
        menuitem = Menuitem.objects.get(pk='contenu1')

        # Le menuitem reference une page de contenu
        self.assertIsInstance(menuitem.page, PageContenu)

        # On change le type de page reference
        page = PageGenerique()
        page.viewname = 's5vitrine.some_view'
        page.save()

        menuitem.page = page
        menuitem.save()

        menuitem_loaded = Menuitem.objects.get(pk='contenu1')
        self.assertIsInstance(menuitem_loaded.page, PageGenerique)
