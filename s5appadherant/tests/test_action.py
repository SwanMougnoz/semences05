# -*- coding: utf-8 -*-
from actstream.actions import follow
from actstream.models import Action
from actstream import action
from actstream.registry import register
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.test import TestCase
from django_dynamic_fixture import G

from s5appadherant.models import Jardin, Cultivateur, Adherant


class S5ActionManagerTest(TestCase):

    def setUp(self):
        self.user = G(User)

    def test_get_by_terms_verb(self):
        action.send(self.user, verb='foo')
        loaded = Action.objects.get_by_terms(verb='foo')
        self.assertEqual('foo', loaded.verb)

    def test_get_by_terms_action_object(self):
        jardin = G(Jardin)
        action.send(self.user, verb='foo', action_object=jardin)

        loaded = Action.objects.get_by_terms(action_object=jardin)
        self.assertEqual(jardin, loaded.action_object)

    def test_get_by_terms_target(self):
        jardin = G(Jardin)
        action.send(self.user, verb='foo', target=jardin)

        loaded = Action.objects.get_by_terms(target=jardin)
        self.assertEqual(jardin, loaded.target)

    def test_get_by_terms_all(self):
        jardin = G(Jardin)
        cultivateur = G(Cultivateur, jardin=jardin)
        action.send(self.user, verb='foo', action_object=cultivateur, target=jardin)

        loaded = Action.objects.get_by_terms(verb='foo', action_object=cultivateur, target=jardin)
        self.assertEqual('foo', loaded.verb)
        self.assertEqual(cultivateur, loaded.action_object)
        self.assertEqual(jardin, loaded.target)

    def test_get_by_terms_not_unique(self):
        action.send(self.user, verb='foo')
        action.send(self.user, verb='foo')

        with self.assertRaises(MultipleObjectsReturned):
            Action.objects.get_by_terms(verb='foo')


class SelfExcludedUnprocessedStreamTest(TestCase):

    def setUp(self):
        self.adherant = G(Adherant)
        self.other_adherant = G(Adherant)
        self.jardin = G(Jardin)

        # Les deux adhérant écoutent l'activité de self.jardin
        follow(self.adherant.user, self.jardin, actor_only=False, send_action=False)
        follow(self.other_adherant.user, self.jardin, actor_only=False, send_action=False)

    def test_unprocessed(self):
        # self.other effectue des actions sur self.jardin
        action.send(self.other_adherant.user, verb='foo', target=self.jardin)
        action.send(self.other_adherant.user, verb='bar', target=self.jardin)

        # self.adherant traite l'action foo
        foo_action = Action.objects.get_by_terms(verb='foo', target=self.jardin)
        self.adherant.processed_actions.add(foo_action)
        self.adherant.save()

        bar_action = Action.objects.get_by_terms(verb='bar', target=self.jardin)

        # Il doit rester uniquement l'action bar dans son flux
        stream = Action.objects.self_excluded_unprocessed(self.adherant.user)
        self.assertEqual(1, stream.count())
        self.assertEqual(bar_action, stream.first())

    def test_self_excluded(self):
        # Les deux adherants effectuent des actions sur self.jardin
        action.send(self.adherant.user, verb='foo', target=self.jardin)
        action.send(self.other_adherant, verb='bar', target=self.jardin)

        bar_action = Action.objects.get_by_terms(verb='bar', target=self.jardin)

        # Le flux doit contenir uniquement l'action de self.other
        stream = Action.objects.self_excluded_unprocessed(self.adherant.user)
        self.assertEqual(1, stream.count())
        self.assertEqual(bar_action, stream.first())



