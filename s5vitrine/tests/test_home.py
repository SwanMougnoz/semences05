from django.test import TestCase


class HomeTest(TestCase):
    def test_get(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 's5vitrine/home.html')