from uuid import uuid4

from django.template.loader import get_template
from table.columns import Link


class ConfirmLink(Link):
    """
    Lien affichant une modal de confirmation avant redirection

    :param modal_template: Doit definir comme id de la modal la valeur modal_id donnee en context et fournir un lien
    avec la class btn-ok pour permettre la rediection
    """

    def __init__(self, modal_template, modal_id, *args, **kwargs):
        super(ConfirmLink, self).__init__(*args, **kwargs)
        self.modal_template = modal_template
        self.modal_id = modal_id

    @property
    def attrs(self):
        if self.url:
            self.base_attrs["data-href"] = self.url
        return self.base_attrs

    def render(self, obj):
        # Ajout d'un identifiant unique pour chaque lien dans la table
        modal_id = u"%s-%s" % (self.modal_id, uuid4())

        self.base_attrs['data-toggle'] = 'modal'
        self.base_attrs['data-target'] = u"#%s" % modal_id

        modal_template = get_template(self.modal_template)
        modal = modal_template.render({
            'modal_id': modal_id
        })

        template = get_template('s5appadherant/table/confirm_link.html')
        context = {
            'link': super(ConfirmLink, self).render(obj),
            'modal': modal,
            'modal_id': modal_id
        }

        return template.render(context)
