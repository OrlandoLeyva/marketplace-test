from django.urls import path
from .views import ProductsList, ProductDetails, ProductReviewsList, ReviewDetails

urlpatterns = [
    path('products/', ProductsList.as_view(), name='products-list'),
    path('products/<int:pk>', ProductDetails.as_view(), name='product-detail'),
    path('products/<int:pk>/reviews/', ProductReviewsList.as_view(), name='product-reviews'),
    path('reviews/<int:pk>/', ReviewDetails.as_view(), name='review-details'),
]
