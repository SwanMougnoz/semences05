# coding=utf-8
from django.apps import AppConfig


class Semences05Config(AppConfig):
    name = 'semences05'

    def ready(self):
        # Methode un peu hacky pour s'assurer que le champs email de de user soit unique
        # Permet de ne pas avoir a redefinir tout un model user
        # /!\ Cette action entraine la génération d'une migration dans contrib.auth
        from django.contrib.auth.models import User
        User._meta.get_field('email')._unique = True
