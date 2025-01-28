# accounts/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Pet
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# class PetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pet
#         fields = ['id', 'name', 'type', 'category', 'breed', 'isPublic', 'additionalInfo', 'photos']

#     def create(self, validated_data):
#         user = self.context['request'].user
#         validated_data['owner'] = user
#         return super().create(validated_data)


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'type', 'category', 'breed', 'isPublic', 
            'additionalInfo', 'animal_id', 'registered_at', 
            'images', 'features', 'owner'
        ]
        read_only_fields = ['animal_id', 'registered_at', 'owner']  # These fields are auto-generated

    def create(self, validated_data):
        # Set the owner to the current user
        validated_data['owner'] = self.context['request'].user

        # Generate a unique animal_id
        validated_data['animal_id'] = f"ANI{Pet.objects.count() + 1:04d}"

        # Create the Pet instance
        # pet = Pet.objects.create(**validated_data)
        # return pet
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Update the Pet instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance