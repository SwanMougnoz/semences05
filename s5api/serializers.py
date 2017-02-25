from rest_framework import serializers

from s5appadherant.models import Jardin, Adresse, Culture, Variete


class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        exclude = []


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
    varietes_cultivees = MapCultureSerializer(source='culture_set', many=True, read_only=True)

    class Meta:
        model = Jardin
        fields = [
            'id',
            'appelation',
            'short_description',
            'varietes_cultivees'
        ]
