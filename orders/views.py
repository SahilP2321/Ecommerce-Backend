from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from cart.models import Cart
from .serializers import OrderSerializer, CreateOrderSerializer

class CreateOrderView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        
        if cart.items.count() == 0:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            # Check stock availability
            for cart_item in cart.items.all():
                if cart_item.quantity > cart_item.product.stock:
                    return Response({
                        'error': f'Insufficient stock for {cart_item.product.name}'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                shipping_address=serializer.validated_data['shipping_address'],
                shipping_city=serializer.validated_data['shipping_city'],
                shipping_state=serializer.validated_data['shipping_state'],
                shipping_country=serializer.validated_data['shipping_country'],
                shipping_pincode=serializer.validated_data['shipping_pincode'],
                payment_method=serializer.validated_data['payment_method'],
                notes=serializer.validated_data.get('notes', ''),
                subtotal=cart.subtotal,
                total=cart.total
            )
            
            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    product_price=cart_item.unit_price,
                    variant=cart_item.variant,
                    variant_name=f"{cart_item.variant.name}: {cart_item.variant.value}" if cart_item.variant else '',
                    quantity=cart_item.quantity,
                    subtotal=cart_item.subtotal
                )
                
                # Update stock
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
                
                if cart_item.variant:
                    cart_item.variant.stock -= cart_item.quantity
                    cart_item.variant.save()
            
            # Clear cart
            cart.items.all().delete()
            
            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def put(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        if order.status not in ['pending', 'processing']:
            return Response({'error': 'Cannot cancel order at this stage'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'cancelled'
        order.save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)