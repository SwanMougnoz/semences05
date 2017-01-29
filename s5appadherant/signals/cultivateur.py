from actstream import action
from actstream.actions import follow
from actstream.models import Action
from django.core.exceptions import ObjectDoesNotExist

from services.mailer import MailFactory


def save_actions(sender, instance, created, **kwargs):
    if created:
        MailFactory.send('cultivateur_request', cultivateur=instance)
        action.send(instance.adherant.user, verb="request", action_object=instance, target=instance.jardin)
        follow(instance.adherant.user, instance, actor_only=False, send_action=False)
    else:
        if instance.accepte:
            MailFactory.send('cultivateur_accept', cultivateur=instance)
            action.send(instance.jardin.proprietaire.user, verb="accept", action_object=instance, target=instance.jardin)
            follow(instance.adherant.user, instance.jardin, actor_only=False, send_action=False)
        else:
            MailFactory.send('cultivateur_deny', cultivateur=instance)
            action.send(instance.jardin.proprietaire.user, verb="deny", action_object=instance, target=instance.jardin)

        try:
            request_action = Action.objects.get_by_terms('request', instance, instance.jardin)
            instance.jardin.proprietaire.processed_actions.add(request_action)
            instance.jardin.proprietaire.save()
        except ObjectDoesNotExist:
            # todo: logger cette action
            pass
