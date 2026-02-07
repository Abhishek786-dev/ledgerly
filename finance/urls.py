from rest_framework.routers import DefaultRouter
from .views import AccountView, PaymentMethodView

router = DefaultRouter()
router.register('accounts', AccountView, basename='accounts')
router.register('payment-methods', PaymentMethodView, basename='payment-methods')

urlpatterns = router.urls