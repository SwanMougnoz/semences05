from django.test import TestCase

from s5appadherant.models import Variete
from s5appadherant.tables.columns import ImageColumn


class ImageColumnTest(TestCase):

    fixtures = ['varietes']

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