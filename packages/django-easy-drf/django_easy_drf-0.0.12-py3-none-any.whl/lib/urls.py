
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register('event', EventViewSet, basename='event')
router.register('perro-grande', PerroGrandeViewSet, basename='perro-grande')
router.register('gato', GatoViewSet, basename='gato')
urlpatterns = router.urls
