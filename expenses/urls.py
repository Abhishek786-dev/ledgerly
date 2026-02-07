from rest_framework.routers import DefaultRouter
from .views import ExpenseView

router = DefaultRouter()
router.register('transaction', ExpenseView, basename='transaction')

urlpatterns = router.urls