from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from orders.models import Order
from .models import Payment
import uuid

class CreatePaymentView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        if order.payment_status == 'completed':
            return Response({'error': 'Payment already completed'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Simulate payment processing
        transaction_id = str(uuid.uuid4())
        
        # In real implementation, integrate with payment gateway here
        # For demo, we'll assume payment is successful
        payment = Payment.objects.create(
            order=order,
            user=request.user,
            amount=order.total,
            payment_method=order.payment_method,
            transaction_id=transaction_id,
            status='success',
            payment_response='{"status": "success"}'
        )
        
        # Update order payment status
        order.payment_status = 'completed'
        order.status = 'processing'
        order.save()
        
        return Response({
            'message': 'Payment successful',
            'transaction_id': transaction_id,
            'amount': order.total
        }, status=status.HTTP_200_OK)

class PaymentStatusView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        try:
            payment = Payment.objects.get(order=order)
            return Response({
                'status': payment.status,
                'transaction_id': payment.transaction_id,
                'amount': payment.amount,
                'payment_method': payment.payment_method,
                'created_at': payment.created_at
            })
        except Payment.DoesNotExist:
            return Response({'status': 'pending'})