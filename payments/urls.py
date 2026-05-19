from django.urls import path
from .views import CreatePaymentView, PaymentStatusView

urlpatterns = [
    path('<int:order_id>/create/', CreatePaymentView.as_view(), name='create-payment'),
    path('<int:order_id>/status/', PaymentStatusView.as_view(), name='payment-status'),
]