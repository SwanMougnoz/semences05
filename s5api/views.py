from rest_framework import generics
from rest_framework import mixins

from s5api.serializers import MapJardinListSerializer, MapJardinDetailSerializer, MapCultureSerializer, \
    MapJardinDetailAdherantSerializer
from s5appadherant.models import Jardin, Culture


class MapJardinListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Jardin.objects.all()
    serializer_class = MapJardinListSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MapJardinDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Jardin.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_authenticated():
            return MapJardinDetailAdherantSerializer
        else:
            return MapJardinDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class MapCultureListView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = MapCultureSerializer

    def get_queryset(self):
        return Culture.objects.filter(jardin_id=self.kwargs['pk'], date_fin__isnull=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
