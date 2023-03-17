from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializer, CartSerializer, ProductSerializer, ProductImageSerializer
from .models import User, Cart, Product, ProductImage
from django.core.mail import send_mail
import random

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            cart = Cart(user=user)
            cart.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class OTPViewSet(viewsets.ViewSet):

    def create(self, request):
        email = request.data.get('email')
        otp = random.randint(100000, 999999)
        send_mail(
            'OTP verification',
            f'Your OTP for verification is {otp}',
            'sender@example.com',
            [email],
            fail_silently=False,
        )
        return Response({'email': email, 'otp': otp})

class LoginViewSet(viewsets.ViewSet):

    def create(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        if otp == '123456': # Replace with your own OTP verification logic
            user = User.objects.get(email=email)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({'detail': 'Invalid OTP'}, status=400)

class CartItemViewSet(viewsets.ViewSet):

    def create(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        cart = user.cart
        cart.add_item(product_id, quantity)
        return Response({'detail': 'Product added to cart'})