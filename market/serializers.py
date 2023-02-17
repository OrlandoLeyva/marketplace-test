from rest_framework import serializers
from .models import Product, Category, Review

# class CategoryStringSerializer(serializers.StringRelatedField):
#     def to_internal_value(self, data):
#         return Category.objects.get(name=data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    # categories = CategorySerializer(many=True)
    # user = ReadOnlyField(source='user.username')
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ['user']
        extra_kwargs = {
            "user":{
                "read_only": True,
                "required": False
            }
        }

    # def create(self, validated_data):
    #     print(validated_data)
    #     raise serializers.ValidationError('This is not a real error')
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('comment', 'rating')


    