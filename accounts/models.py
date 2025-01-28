# from django.contrib.auth.models import User
# from django.db import models

# class Pet(models.Model):
#     name = models.CharField(max_length=100)
#     type = models.CharField(max_length=100)
#     category = models.CharField(max_length=100)
#     breed = models.CharField(max_length=100)
#     isPublic = models.BooleanField(default=False)  # 'isPublic' field name
#     additionalInfo = models.TextField(null=True, blank=True)
#     photos = models.ImageField(upload_to='pet_photos/')
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinLengthValidator, RegexValidator
import json

# Define validation functions outside the model
def validate_json_dict(value):
    """Ensure value is a JSON-serializable dictionary"""
    if not isinstance(value, dict):
        raise ValueError("Must be a dictionary")
    json.dumps(value)  # Test JSON serialization

def validate_json_list(value):
    """Ensure value is a JSON-serializable list"""
    if not isinstance(value, list):
        raise ValueError("Must be a list")
    json.dumps(value)  # Test JSON serialization

class Pet(models.Model):
    CATEGORY_CHOICES = [
        ('Domestic', 'Domestic'),
        ('Wild', 'Wild'),
        ('Exotic', 'Exotic'),
        ('Farm', 'Farm')
    ]

    # Required fields with validation
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r'^[a-zA-Z0-9 \'-]+$',
                message='Name can only contain letters, numbers, spaces, apostrophes, and hyphens'
            )
        ]
    )
    type = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r'^[a-zA-Z ]+$',
                message='Type can only contain letters and spaces'
            )
        ]
    )
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )
    breed = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r'^[a-zA-Z ]+$',
                message='Breed can only contain letters and spaces'
            )
        ]
    )
    
    # JSON fields with validation
    additionalInfo = models.JSONField(
        default=dict,
        validators=[validate_json_dict]
    )
    images = models.JSONField(
        default=list,
        validators=[validate_json_list]
    )
    features = models.JSONField(
        default=list,
        validators=[validate_json_list]
    )
    
    # System-managed fields
    isPublic = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pets'
    )
    animal_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.animal_id})"

    def save(self, *args, **kwargs):
        # Generate animal_id if not set
        if not self.animal_id:
            last_pet = Pet.objects.order_by('-id').first()
            if last_pet and last_pet.animal_id:
                last_id = int(last_pet.animal_id[3:])
            else:
                last_id = 0
            self.animal_id = f"ANI{last_id + 1:04d}"
        
        # Type enforcement
        if not isinstance(self.additionalInfo, dict):
            self.additionalInfo = {}
        if not isinstance(self.images, list):
            self.images = []
        if not isinstance(self.features, list):
            self.features = []
            
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['animal_id']),
            models.Index(fields=['owner']),
        ]
        ordering = ['-registered_at']