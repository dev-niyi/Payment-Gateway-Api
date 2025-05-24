import uuid
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerialzer
# Create your views here.

class PaymentCreateView(APIView):
    def post(self, request):
        serializer = PaymentSerialzer(data = request.data)
        if serializer.is_valid():
            reference = str(uuid.uuid4())
            amount_to_kobo = int(serializer.validated_data["amount"] * 100)

            data = {
                    # based on the parameters to be provided by paystack
                    "email" : serializer.validated_data["email"],
                    "amount" : amount_to_kobo,
            }

            headers = {
                   "Authorization" : f"Bearer {settings.PAY_STACK_SECRET_KEY}",
                   "Content-Type" : "application/json",
            }
            
            paystack_url = "https://api.paystack.co/transaction/initialize"
            response = requests.post(paystack_url, json = data, headers = headers,)
            print("Paystack Response Status:", response.status_code)
            print("Paystack Response Content:", response.text)

            if response.status_code == 200:
                serializer.save(reference = reference, status = "pending")
                auth_url = response.json()["data"]["authorization_url"]
                return Response ({
                    "Payment" : serializer.data,
                    'authorization_url' : auth_url},
                     status = status.HTTP_200_OK
                )
            
            return Response({
                "ErrorMessage" : "Failed initialized payment"},
                 status = status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'ErrorMessage' : "Bad Request"},
            serializer.errors, status = status.HTTP_400_BAD_REQUEST
        )
    
#gets the status of the payment
class PaymentStatus(APIView):
    def get(self, request, pk):
            try:
                payment = Payment.objects.get(pk = pk)
            except Payment.DoesNotExist:
                return Response({
                    "errors" : "Payment doesn't exist"},
                    status = status.HTTP_404_NOT_FOUND
                )

            verify_url = f"https://api.paystack.co/transaction/verify/{payment.reference}"

            headers = {
                "Authorization" : f"Bearer {settings.PAY_STACK_SECRET_KEY}",
                "Content-Type" : "application/json"
            }

            response = requests.get(verify_url, headers=headers)
            if response.status_code == 200:
                result = response.json()["data"]["status"]
                payment.status = result
                payment.save()

                return Response ({
                    "Payment" : PaymentSerialzer(payment).data,
                    "paystack_stack" : result
                    }, status  =  status.HTTP_200_OK
                )
            return Response ({
                    "error" : "Failed to verufy payment"},
                    status = status.HTTP_400_BAD_REQUEST
            )
        