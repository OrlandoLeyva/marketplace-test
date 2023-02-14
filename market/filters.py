from rest_framework import filters
from .models import Category

class ProductsPriceFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        if min_price and max_price:
            return queryset.filter(price__gte = min_price, price__lte = max_price)
        elif min_price:
            return queryset.filter(price__gte = min_price)
        elif max_price:
            return queryset.filter(price__lte = max_price)
        return queryset

class IsAvailableProductFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(available=True)

class ProductCategoryFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category = request.query_params.get('category')
        category_queryset = Category.objects.get(name = category)
        if not category:
            return queryset
        return [ product for product in queryset if category_queryset in product.categories.all()]

class ProductReviewRatingFilterBackend(filters.BaseFilterBackend):
    '''
    Filter movie reviews by rating
    '''
    def filter_queryset(self, request, queryset, view):
        print('rating...')
        rating = request.query_params.get('rating')
        if not rating:
            return queryset
        return queryset.filter(rating=rating)

#* To implement this filter is necessary first add the rating_avg filed to each product.  
# class ProductReviewRatingFilterBackend(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         rating = request.query_params.get('rating')
#         if rating:
#           return [product for product in queryset if product.reviews.rating == rating]
#         return super().filter_queryset(request, queryset, view)
