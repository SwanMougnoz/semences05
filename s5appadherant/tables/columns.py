# -*- coding: utf-8 -*-
from django.template import Context
from django.template import Template
from django.template.loader import get_template
from table.columns import LinkColumn
from table.utils import Accessor
from table.columns import Column


class ImageColumn(Column):
    def render(self, obj):
        image = Accessor(self.field).resolve(obj)
        template = Template("""
            {% load static %}
            {% if image %}
                <img class="img-responsive" src="{{ image.url }}">
            {% else %}
                <img class="img-responsive" src="{% static 's5appadherant/images/no_image.png' %}">
            {% endif %}
        """)

        return template.render(Context({
            'image': image
        }))


class DropDownLinkColumn(LinkColumn):
    def render(self, obj):
        template = get_template('s5appadherant/partials/table.dropdown_column.html')

        button_link = self.links[0]
        button_link.base_attrs.update({
            'class': 'btn btn-default'
        })
        button_link = button_link.render(obj)

        dropdown_links = [btn.render(obj) for btn in self.links[1:]]

        return template.render(Context({
            'button_link': button_link,
            'dropdown_links': dropdown_links
        }))