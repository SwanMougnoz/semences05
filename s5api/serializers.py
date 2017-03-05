from django.contrib.auth.models import User
from rest_framework import serializers

from s5appadherant.models import Jardin, Adresse, Culture, Variete, Adherant


class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        exclude = []


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]


class AdherantSerializer(serializers.ModelSerializer):
    user = UserNameSerializer(many=False)
    adresse = AdresseSerializer(many=False)

    class Meta:
        model = Adherant
        exclude = [
            'processed_actions'
        ]


class MapAdherantSerializer(serializers.ModelSerializer):
    user = UserNameSerializer(read_only=True, many=False)

    class Meta:
        model = Adherant
        fields = [
            'id',
            'user',
        ]


class MapVarieteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variete
        fields = [
            'id',
            'nom',
            'short_description'
        ]


class MapCultureSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        variete_rep = MapVarieteSerializer(instance=instance.variete)
        return variete_rep.data

    class Meta:
        model = Culture
        fields = [
            'variete'
        ]


class MapJardinListSerializer(serializers.ModelSerializer):
    adresse = AdresseSerializer(read_only=True)

    class Meta:
        model = Jardin
        fields = [
            'id',
            'appelation',
            'adresse'
        ]


class MapJardinDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jardin
        fields = [
            'id',
            'appelation',
            'short_description'
        ]


class MapJardinDetailAdherantSerializer(MapJardinDetailSerializer):
    proprietaire = MapAdherantSerializer(read_only=True, many=False)

    class Meta:
        model = Jardin
        fields = [
            'id',
            'appelation',
            'short_description',
            'proprietaire'
        ]
