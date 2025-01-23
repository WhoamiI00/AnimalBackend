from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from animals.models import Animal  # Correctly import the `Animal` model
from animals.serializers import AnimalSerializer  # Correctly import the `AnimalSerializer`


class AnimalsViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()  # Use `Animal` model
    serializer_class = AnimalSerializer  # Use `AnimalSerializer`
    permission_classes = [AllowAny]
