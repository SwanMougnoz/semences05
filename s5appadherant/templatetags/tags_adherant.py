# -*- coding: utf-8 -*-
from actstream.templatetags.activity_tags import AsNode
from django import template
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

register = template.Library()


@login_required()
@register.inclusion_tag('s5appadherant/partials/tag.menu_adherant.html')
def menu_adherant(request, menu_actif=None):

    user = request.user
    if not user.first_name or not user.last_name:
        username = 'Accueil'
    else:
        username = u'%s %s' % (user.first_name, user.last_name)

    return {
        'request': request,
        'username': username,
        'menu_actif': menu_actif
    }


class DisplayActivityRow(AsNode):

    def render_result(self, context):
        action_instance = context['action'] = self.args[0].resolve(context)
        verb = action_instance.verb.replace(' ', '_')

        templates = [
            'actstream/%s.html' % verb,
            'actstream/action.html',
        ]

        if action_instance.action_object:
            templates.insert(
                0,
                'actstream/%s/%s.html' % (action_instance.action_object_content_type.name, verb)
            )

        return render_to_string(templates, context)


@login_required()
@register.tag()
def activity_row(parser, token):
    """
    Affiche une action activity stream
    Surcharge actstream.display_action pour chercher des templates spécifiques au type d'action_object en plus du verbe
    """
    return DisplayActivityRow.handle_token(parser, token)
