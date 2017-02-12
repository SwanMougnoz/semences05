from django.apps import AppConfig


class S5appadherantConfig(AppConfig):
    name = 's5appadherant'

    def ready(self):
        from actstream import registry
        from django.contrib.auth.models import User

        registry.register(User)
        registry.register(self.get_model('Jardin'))
        registry.register(self.get_model('Adherant'))
        registry.register(self.get_model('Cultivateur'))
        registry.register(self.get_model('Culture'))
