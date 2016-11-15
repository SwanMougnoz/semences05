from django.test import TestCase
from django.core.urlresolvers import resolve
from s5vitrine.models import  PageGenerique, PageContenu


class PageGeneriqueTest(TestCase):
    def test_url(self):
        # Test avec un objet vide
        page = PageGenerique()
        self.assertIsNone(page.url)

        # Test sans parametres
        page = PageGenerique()
        page.viewname = 's5vitrine.accueil_view'
        reversed_url = page.url
        # On verifie que l'URL retournee correspond a la vue specifiee
        resolved = resolve(reversed_url)
        self.assertEqual('s5vitrine.accueil_view', resolved.view_name)

        # Test avec des parametres
        page = PageGenerique()
        page.viewname = "s5vitrine.contenu_view"
        page.params = "1"
        reversed_url = page.url
        resolved = resolve(reversed_url)
        self.assertEqual('s5vitrine.contenu_view', resolved.view_name)
        self.assertEqual({
            "contenu_id": u'1'
        }, resolved.kwargs)


class PageContenuTest(TestCase):
    def test_url(self):
        # Test avec un objet vide
        page = PageContenu()
        self.assertIsNone(page.url)

        # Test avec un id
        page.save()
        reversed_url = page.url
        resolved = resolve(reversed_url)
        self.assertEqual('s5vitrine.contenu_view', resolved.view_name)
        self.assertEqual({
            "contenu_id": u'1'
        }, resolved.kwargs)
