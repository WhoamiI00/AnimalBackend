from rest_framework import routers

from animals.viewsets import AnimalsViewSet

router = routers.SimpleRouter()

router.register(r'animals', AnimalsViewSet, basename="animals")

urlpatterns = router.urls