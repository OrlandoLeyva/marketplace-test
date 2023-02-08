from django.shortcuts import render
#* Rest_framework
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
#* Models and serializers
from .models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer

# Create your views here.
class ProductsList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)