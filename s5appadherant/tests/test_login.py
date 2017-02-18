from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from s5appadherant.forms.login import LoginForm


class LoginViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def isLoggedInAs(self, user):
        client_user = auth.get_user(self.client)
        return client_user.__eq__(user)

    def test_get(self):
        response = self.client.get(reverse('s5appadherant:login'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LoginForm)
        self.assertTemplateUsed(response, 's5appadherant/login/form.html')

    def test_post_login_ok(self):
        # Test avec un formulaire valide
        response = self.client.post(reverse('s5appadherant:login'), data={
            'email': 'lennon@thebeatles.com',
            'password': 'johnpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.isLoggedInAs(self.user))
        self.assertEqual(reverse('s5appadherant:accueil'), response.url)

    def test_post_login_failed(self):
        # Test avec un formulaire invalide
        response = self.client.post(reverse('s5appadherant:login'), data={
            'email': 'fake@email.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.isLoggedInAs(self.user))
        self.assertTemplateUsed(response, 's5appadherant/login/form.html')
        self.assertTrue(response.context['on_error'])
        self.assertIn('message', response.context)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def isLoggedInAs(self, user):
        client_user = auth.get_user(self.client)
        return client_user.__eq__(user)

    def test_get(self):
        self.client.post(reverse('s5appadherant:login'), data={
            'email': 'lennon@thebeatles.com',
            'password': 'johnpassword'
        })
        self.assertTrue(self.isLoggedInAs(self.user))
        self.client.get(reverse('s5appadherant:logout'))
        self.assertFalse(self.isLoggedInAs(self.user))




