from django.contrib.auth.models import User
from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    isPublic = models.BooleanField(default=False)  # 'isPublic' field name
    additionalInfo = models.TextField(null=True, blank=True)
    photos = models.ImageField(upload_to='pet_photos/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)