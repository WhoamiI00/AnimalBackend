from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from animals.models import Animals

from animals.serializers import AnimalsSerializer


class AnimalsViewSet(viewsets.ModelViewSet):
    queryset = Animals.objects.all()
    serializer_class = AnimalsSerializer
    permission_classes = [AllowAny]