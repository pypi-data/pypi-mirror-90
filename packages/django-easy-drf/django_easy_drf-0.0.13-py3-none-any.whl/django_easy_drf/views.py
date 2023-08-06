
from rest_framework import viewsets
from .serializers import *
from .models import *

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class PerroGrandeViewSet(viewsets.ModelViewSet):
    queryset = PerroGrande.objects.all()
    serializer_class = PerroGrandeSerializer

class GatoViewSet(viewsets.ModelViewSet):
    queryset = Gato.objects.all()
    serializer_class = GatoSerializer
