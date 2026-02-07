from rest_framework.routers import DefaultRouter
from .views import CategoryView, VendorView

router = DefaultRouter()
router.register('list', CategoryView, basename='categories')
router.register('vendors', VendorView, basename='vendors')

urlpatterns = router.urls