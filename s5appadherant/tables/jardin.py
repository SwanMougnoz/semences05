# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy

from s5appadherant.models import Jardin, Adherant
from table import Table
from table.utils import A
from table.columns import Link
from table.columns import Column, LinkColumn


class ProfilJardinTable(Table):
    appelation = Column(field='appelation', header='Appelation')
    proprietaire = LinkColumn(field='proprietaire',
                              header='Proprietaire',
                              links=[Link(
                                  text=A('proprietaire.user.first_name'),
                                  viewname='s5appadherant:profil_detail',
                                  args=(A('proprietaire.id'),)
                              )])
    commune = Column(field='adresse.commune', header='Commune')
    exposition = Column(field='exposition', header='Exposition')
    type_sol = Column(field='type_sol', header='Type de sol')
    irrigation = Column(field='irrigation', header='Irrigation')
    superficie = Column(field='superficie', header='Superficie')
    mise_en_culture = Column(field='mise_en_culture', header='Mise en culture')
    action = LinkColumn(header='Action',
                        sortable=False,
                        links=[Link(
                            text='Détail',
                            viewname='s5appadherant:jardin_detail',
                            args=(A('id'),)
                        )])

    def __init__(self, *args, **kwargs):
        adherant = kwargs.pop('adherant', None)
        if not isinstance(adherant, Adherant):
            raise ValueError(u'ProfilJardinTable: aucun adhérant défini')

        super(ProfilJardinTable, self).__init__(*args, **kwargs)

        self.opts.ajax_source = reverse_lazy('s5appadherant:profil_jardin_data', kwargs={
            'adherant_id': adherant.id
        })
        self.opts.page_length = 5

    class Meta:
        search = False
        pagination_next = 'Suivant'
        pagination_prev = 'Précédent'
        zero_records = "Aucun jardin cultivé"
        ajax = True
        model = Jardin
        attrs = {'class': 's5-table table-bordered table-hover table-striped'}
