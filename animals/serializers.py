from rest_framework import serializers

from animals.models import Animals


class AnimalsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animals
        fields = ['name', 'age', 'type', 'breed', 'id']
        read_only_fields = ['created', 'updated', 'id']