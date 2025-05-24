from django.urls import path 
from .views import  PaymentCreateView, PaymentStatus

urlpatterns = [
    path('payments/', PaymentCreateView.as_view(), name='initiate-payment'),
    path('payments/<str:reference>/', PaymentStatus.as_view(), name = "payment-status"),
]