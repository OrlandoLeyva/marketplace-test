from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Product, Category, Review

from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

class ProductsTestCase(APITestCase):
    def setUp(self) -> None:
        # Register user
        self.user = User.objects.create(username='test', password='test')
        # Get token
        self.token = Token.objects.get_or_create(user=self.user)[0]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # Create category
        self.category = Category.objects.create(name='general')
        # Create product
        product_data = {
            'name': 'default product', 
            'description': 'description test',
            'price': 1,
            'user': self.user,
            'available': True
        }
        self.product = Product(**product_data)
        self.product.save()
        self.product.categories.add(self.category)

    def test_create_product(self):
        '''Create product test case'''
        product_data = {
            'name': 'product test', 
            'description': 'description test',
            'price': 1,
            'available': True,  
            'categories': [self.category.id],
        }

        response = self.client.post(reverse('products_list'), product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_products(self):
        '''List all products test case'''
        response = self.client.get(reverse('products_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_details(self):
        '''Get product details'''
        response = self.client.get( reverse( 'product_details', args=(self.product.id, ) ) )
        # response = self.client.get(reverse('product_details', args=(self.product.id,)))
        print('Product ', response.content)
        self.assertEqual(response.status_code, 200)

    def test_product_reviews_list(self):
        '''Product reviews test case'''
        response = self.client.get(reverse('product_reviews', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_product_reviews_create(self):
        '''Product create review test case'''
        review = { 
            'comment': 'great product',
            'rating': 5,
        }
        response = self.client.post(reverse('product_reviews', args=[self.product.id]), review)
        self.assertEqual(response.status_code, 201)

class ReviewsTestCase(APITestCase):
    def setUp(self) -> None:
        # Create user
        self.user = User.objects.create(username='test', password='test')
        self.category = Category.objects.create(name='category')
        # Create product
        product_data = {
            'name': 'default product', 
            'description': 'description test',
            'price': 1,
            'user': self.user,
            'available': True
        }
        self.product = Product(**product_data)
        self.product.save()
        self.product.categories.add(self.category)
        # Create review
        review = {
            'comment': 'good',
            'rating': 5,
            'user': self.user,
            'product': self.product
        }
        self.review = Review.objects.create(**review)

    def test_reviews_list(self):
        '''List all reviews test case'''
        response = self.client.get(reverse('reviews_list'))
        self.assertEqual(response.status_code, 200)

    def test_reviews_create(self):
        '''Create a through the wrong URL'''
        review = { 
            'comment': 'great product',
            'rating': 5,
        }

        response = self.client.post(reverse('reviews_list'), review)
        self.assertEqual(response.status_code, 405)

    def test_review_details(self):
        '''Review details test case'''
        response = self.client.get(reverse('review_details', args=[self.review.id]))
        self.assertEqual(response.status_code, 200, msg='THis is the rw test, bitch')
        self.ass
    
#review_details
#reviews_list