from django.apps import AppConfig
from django.db.models.signals import post_save


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

        from s5appadherant.signals import cultivateur

        post_save.connect(cultivateur.save_actions,
                          sender=self.get_model('Cultivateur'),
                          dispatch_uid="cultivateur:post_save")
