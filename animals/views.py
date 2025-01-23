import os
import cv2
import numpy as np
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from .models import Animal
from .serializers import AnimalSerializer

# Initialize MobileNetV2 model
try:
    mobilenet_model = MobileNetV2(weights='imagenet', include_top=True)
except Exception as e:
    mobilenet_model = None
    print(f"Error loading MobileNetV2 model: {e}")

def enhance_image(image):
    try:
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        image_uint8 = (image * 255).astype(np.uint8)
        enhanced_channels = [clahe.apply(channel) for channel in cv2.split(image_uint8)]
        return cv2.merge(enhanced_channels)
    except Exception as e:
        print(f"Error enhancing image: {e}")
        return image

def extract_features(image):
    try:
        resized = cv2.resize(image, (224, 224))
        preprocessed = preprocess_input(np.expand_dims(resized, axis=0))
        features = mobilenet_model.predict(preprocessed, verbose=0).flatten()
        normalized = features / (np.linalg.norm(features) + 1e-7)
        return normalized.tolist()
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

def compare_features(features1, features2):
    try:
        f1, f2 = np.array(features1), np.array(features2)
        return float(np.dot(f1, f2) / (np.linalg.norm(f1) * np.linalg.norm(f2) + 1e-7))
    except Exception:
        return 0.0

@api_view(['POST'])
def register_animal(request):
    try:
        files = request.FILES.getlist('images')
        if not files:
            return Response({'success': False, 'error': 'No images provided'}, status=400)
  
        animal_id = f"ANI{Animal.objects.count() + 1:04d}"
        saved_images, features_list = [], []

        for file in files:
            # Save the file using default_storage
            filename = f"{animal_id}_{now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = default_storage.save(os.path.join(settings.MEDIA_ROOT, filename), file)
            full_path = default_storage.path(filepath)  # Get the full path of the saved file

            # Check if the file is saved correctly
            if not os.path.exists(full_path):
                print(f"File not found: {full_path}")
                continue

            # Read the image
            image = cv2.imread(full_path)
            if image is None:
                print(f"Error reading image: {full_path}")
                continue

            # Enhance the image
            enhanced = enhance_image(image)
            if enhanced is None or np.count_nonzero(enhanced) == 0:
                print(f"Error enhancing image: {full_path}")
                continue

            # Extract features
            features = extract_features(enhanced)
            if features is None:
                print(f"Error extracting features for image: {full_path}")
                continue

            # Add the image and its features to the lists
            saved_images.append(filename)
            features_list.append(features)

        if not saved_images:
            return Response({'success': False, 'error': 'No valid images processed'}, status=400)

        # Prepare animal data for serialization
        animal_data = {
            'animal_id': animal_id,
            'images': saved_images,
            'features': features_list,
        }
        serializer = AnimalSerializer(data=animal_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'animal_id': animal_id, 'num_images': len(saved_images)})
        return Response({'success': False, 'error': serializer.errors}, status=400)

    except Exception as e:
        print(f"Error in register_animal: {e}")
        return Response({'success': False, 'error': str(e)}, status=500)

@api_view(['POST'])
def search_animal(request):
    try:
        files = request.FILES.getlist('images')
        if not files:
            return Response({'success': False, 'error': 'No images provided'}, status=400)

        search_features = []
        for file in files:
            filepath = default_storage.save(os.path.join(settings.MEDIA_ROOT, file.name), file)
            full_path = default_storage.path(filepath)  # Get the full path of the saved file

            # Check if the file is saved correctly
            if not os.path.exists(full_path):
                print(f"File not found: {full_path}")
                continue

            # Read the image
            image = cv2.imread(full_path)
            if image is None:
                print(f"Error reading image: {full_path}")
                continue

            # Enhance the image
            enhanced = enhance_image(image)
            if enhanced is None or np.count_nonzero(enhanced) == 0:
                print(f"Error enhancing image: {full_path}")
                continue

            # Extract features
            features = extract_features(enhanced)
            if features is None:
                print(f"Error extracting features for image: {full_path}")
                continue

            # Add the extracted features to the search list
            search_features.append(features)

        if not search_features:
            return Response({'success': False, 'error': 'No valid features extracted'}, status=400)

        results, threshold = [], 0.7
        for animal in Animal.objects.all():
            max_similarity = max(
                compare_features(search_feature, stored_feature)
                for search_feature in search_features
                for stored_feature in animal.features
            )
            if max_similarity > threshold:
                results.append({
                    'animal_id': animal.animal_id,
                    'similarity': max_similarity,
                    'images': animal.images,
                    'registered_at': animal.registered_at
                })

        results.sort(key=lambda x: x['similarity'], reverse=True)
        return Response({'success': True, 'matches': results[:5]})
    except Exception as e:
        print(f"Error in search_animal: {e}")
        return Response({'success': False, 'error': str(e)}, status=500)
