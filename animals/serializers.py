from rest_framework import serializers
from .models import Animal  # Correctly import the `Animal` model


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['animal_id', 'registered_at', 'images', 'features']
