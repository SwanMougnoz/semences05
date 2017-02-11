# coding=utf-8
import lxml.html
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_dynamic_fixture import G
from table.columns import Link
from with_asserts.mixin import AssertHTMLMixin

from s5appadherant.models import Variete, Adherant
from s5appadherant.tables.columns import ImageColumn, DropDownLinkColumn
from s5appadherant.tables.fields import ConfirmLink


class ImageColumnTest(TestCase):

    def setUp(self):
        [G(Variete) for i in range(1, 5)]

    def test_render(self):
        variete = Variete.objects.first()
        column = ImageColumn(field='photo')

        expected_output = '<img class="img-responsive" src="%s">' % variete.photo.url
        self.assertHTMLEqual(expected_output, column.render(variete))

    def test_render_no_photo(self):
        variete = Variete()
        column = ImageColumn(field='photo')

        expected_output = '<img class="img-responsive" src="/static/s5appadherant/images/no_image.png">'
        self.assertHTMLEqual(expected_output, column.render(variete))


class DropDownLinkColumnTest(TestCase, AssertHTMLMixin):

    def test_render(self):
        # Bouton tout pourri qui affiche "Accueil -> [ Jardins, Variétés ]"
        column = DropDownLinkColumn(links=[
            Link(text=u'Main button',
                 viewname='s5appadherant:accueil'),
            Link(text=u'Jardins',
                 viewname='s5appadherant:jardin_all',
                 args=()),
            Link(text=u'Variété',
                 viewname='s5appadherant:variete_list')
        ])

        output = column.render(G(Adherant))
        html = lxml.html.fromstring(output)

        elements = html.cssselect(".btn-group > a")
        self.assertEqual(1, len(elements))
        self.assertEqual(u'Main button', elements[0].text)
        self.assertEqual(reverse('s5appadherant:accueil'), elements[0].attrib['href'])

        elements = html.cssselect("button.dropdown-toggle")
        self.assertEqual(1, len(elements))
        self.assertEqual('dropdown', elements[0].attrib['data-toggle'])

        elements = html.cssselect("ul.dropdown-menu li a")
        self.assertEqual(2, len(elements))
        self.assertEqual(u'Jardins', elements[0].text)
        self.assertEqual(reverse('s5appadherant:jardin_all'), elements[0].attrib['href'])
        self.assertEqual(u'Variété', elements[1].text)
        self.assertEqual(reverse('s5appadherant:variete_list'), elements[1].attrib['href'])


class ConfirmLinkTest(TestCase):

    def get_column(self):
        return ConfirmLink(
            text=u"Accueil",
            modal_template='s5appadherant/jardin/partials/modal.delete_culture.html',
            modal_id='mymodal',
            viewname='s5appadherant:accueil'
        )

    def test_attrs(self):
        column = self.get_column()

        with self.assertRaises(KeyError):
            var = column.attrs['href']
        self.assertDictContainsSubset({
            'data-href': reverse('s5appadherant:accueil')
        }, column.attrs)

    def test_render(self):
        column = self.get_column()

        output = column.render(G(Adherant))
        html = lxml.html.fromstring(output)

        elements = html.cssselect('a[data-toggle="modal"]')
        self.assertEqual(1, len(elements))
        self.assertEqual(u"Accueil", elements[0].text)

        modal_id = elements[0].attrib['data-target']
        modal = html.cssselect(u'[id="%s"]' % modal_id[1:])
        self.assertEqual(1, len(modal))
