# -*- coding: utf-8 -*-
from django.template import Context
from django.template import Template
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
