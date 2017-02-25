from rest_framework import generics
from rest_framework import mixins

from s5api.serializers import MapJardinListSerializer, MapJardinDetailSerializer
from s5appadherant.models import Jardin


class MapJardinListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Jardin.objects.all()
    serializer_class = MapJardinListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MapJardinDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Jardin.objects.all()
    serializer_class = MapJardinDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
