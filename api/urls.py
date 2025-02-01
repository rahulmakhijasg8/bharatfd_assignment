from rest_framework.routers import DefaultRouter
from .views import FAQViewSet


router = DefaultRouter()
router.register('faqs', FAQViewSet, basename='FAQ')

urlpatterns = router.urls
