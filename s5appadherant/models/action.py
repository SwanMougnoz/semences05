from actstream.models import Action
from django.db import models


class ProcessedAction(models.Model):
    action = models.OneToOneField(Action, primary_key=True, related_name='processed')


class S5Action(Action):

    def process(self):
        processed = ProcessedAction()
        processed.action = self
        processed.save()

    class Meta:
        proxy = True
