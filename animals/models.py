from django.db import models


class Animal(models.Model):
    animal_id = models.CharField(max_length=20, unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    images = models.JSONField()  # Stores list of image filenames
    features = models.JSONField()  # Stores extracted features as JSON

    def __str__(self):
        return self.animal_id
