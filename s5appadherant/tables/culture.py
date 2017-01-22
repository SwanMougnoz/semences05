# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy

from s5appadherant.models import Culture, Jardin
from table import Table
from table.utils import A
from table.columns import Link
from table.columns import Column, DatetimeColumn, LinkColumn

from s5appadherant.tables.columns import ImageColumn


class CultureTable(Table):
    photo = ImageColumn(field='variete.photo', header='Photo', sortable=False)
    appelation = Column(field='variete.nom', header='Appelation')
    date_debut = DatetimeColumn(field='date_debut', header='Cultivée depuis', format="%d %B %Y")
    type_conservation = Column(field='type_conservation', header='Type de conservation')
    action = LinkColumn(header='Action',
                        sortable=False,
                        links=[Link(
                            text='Fiche variété',
                            viewname='s5appadherant:variete_detail',
                            args=(A('variete.id'),))])

    def __init__(self, *args, **kwargs):
        jardin = kwargs.pop('jardin', None)
        if not isinstance(jardin, Jardin):
            raise ValueError("CultureTable: aucun jardin défini")

        super(CultureTable, self).__init__(*args, **kwargs)

        self.opts.ajax_source = reverse_lazy('s5appadherant:culture_data', kwargs={
            'jardin_id': jardin.id
        })
        self.opts.page_length = 5

    class Meta:
        search = False
        pagination_next = 'Suivant'
        pagination_prev = 'Précédent'
        zero_records = "Aucune variété n'est cultivée dans ce jardin"
        ajax = True
        model = Culture
        attrs = {'class': 's5-table table-bordered table-hover table-striped'}
