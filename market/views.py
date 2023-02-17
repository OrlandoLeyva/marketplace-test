from django.shortcuts import render
#* Rest_framework
from rest_framework import status, generics, permissions, exceptions, filters
from rest_framework.response import Response
#* Models and serializers
from .models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
#* Custom permissions
from .permissions import IsOwnerOrReadOnly
#*Throttles
from rest_framework.throttling import AnonRateThrottle
from .throttling import ReviewDetailsThrottle
#*Filtering
from django_filters.rest_framework import DjangoFilterBackend
from .filters import (ProductsPriceFilterBackend, ProductCategoryFilterBackend, ProductReviewRatingFilterBackend)
#*Pagination
from rest_framework.pagination import LimitOffsetPagination
from .pagination import ProductsPagination, ProductsPaginationOffsetLimit, ProductsCursorPagination

# Create your views here.

class ProductsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [ProductsPriceFilterBackend, filters.SearchFilter, ProductCategoryFilterBackend]
    # ordering_fields = ['name']
    search_fields = ['name']
    # pagination_class = ProductsPagination
    # pagination_class = ProductsPaginationOffsetLimit
    pagination_class = ProductsCursorPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
    '''
    Enable Product to be viewed, updated and deleted
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class ProductReviewsList(generics.ListCreateAPIView):
    '''
    List all reviews of a specific product, or create a new review for it.
    '''
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [ProductReviewRatingFilterBackend]

    def get_queryset(self):
        product_pk = self.kwargs['pk']
        product = Product.objects.get(pk=product_pk)
        print(product)
        return Review.objects.filter(product=product)
        # return Review.objects.all()

    def perform_create(self, serializer):
        product_pk = self.kwargs['pk']
        product = Product.objects.get(pk=product_pk)
        user = self.request.user
        if Review.objects.filter(user=user, product=product).exists():
            raise exceptions.ValidationError(detail='You have already written a review for this product!')
        serializer.save(product=product, user=user)

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    throttle_classes = [ReviewDetailsThrottle]

class ReviewsList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes = [AnonRateThrottle]
    filter_backends = []

    