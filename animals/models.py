from django.db import models

class Animals(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    type = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)