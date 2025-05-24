from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Payment

# Create your tests here.
class PaymentAPITest(APITestCase):
    def setUp(self):
        self.payment = Payment.objects.create(
            name = "Abdul Raqeeb",
            email = "abdulraqeebsaheed@gmail.com",
            amount = 300.00,
            reference = "payment-ref-1234",
            status = "pending",
            CreatedAt = "2025-05-24T00:00:00Z",
        )

        self.post_url = reverse('initiate-payment') 
        self.get_url = reverse('payment-status', kwargs = {'pk': self.payment.pk}) 

    def test_create_payment_valid(self):
        data = {
            "email" : "abdulraqeebsaheed@gmail.com",
            "amount" : "300.00"
        }

        response = self.client.post(self.post_url, data, format = "json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("payment", response.data)
        self.assertIn("authorization_url", response.data)

    def test_missing_field(self):
        data = {
            # the email is missing
            "amount" : "3000.00"
        }

        response = self.client.post(self.post_url, data, format ="json")
        self.assertEqual(response.status_code, status = status.HTTP_400_BAD_REQUEST)

    def test_get_payment_status(self):
        response = self.client.get(self.get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Payment", response.data)
        self.assertIn("paystack_status", response.data) 


    def test_get_payment_not_found(self):
        url = reverse('payment-detail', kwargs={'pk': 9999})  # non-existent payment
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)