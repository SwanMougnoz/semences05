# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser

from models import Adherant


def adherant(request):
    """
    Injecte l'objet Adherant coorespondant à l'utilisateur authentifié
    :param request:
    :return:
    """
    context = {}
    if request.resolver_match.app_name == 's5appadherant' and not isinstance(request.user, AnonymousUser):
        context.update({
            'current_adherant': Adherant.objects.get_from_user(request.user)
        })
    return context
