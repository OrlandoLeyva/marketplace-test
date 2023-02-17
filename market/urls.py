from django.urls import path
from .views import ProductsList, ProductDetails, ProductReviewsList, ReviewDetails, ReviewsList

urlpatterns = [
    path('products/', ProductsList.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetails.as_view(), name='product_details'),
    path('products/<int:pk>/reviews/', ProductReviewsList.as_view(), name='product_reviews'),

    path('reviews/<int:pk>/', ReviewDetails.as_view(), name='review_details'),
    path('reviews/', ReviewsList.as_view(), name='reviews_list'),
]
