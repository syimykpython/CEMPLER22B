from rest_framework import serializers
from .models import Category, Product, Review
from common.validators import validate_age_for_product

# -------------------- Категории --------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

# -------------------- Продукты --------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'category')

    def validate(self, data):
        request = self.context.get('request')
        validate_age_for_product(request)
        return data

class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = serializers.StringRelatedField(many=True)
    class Meta:
        model = Product
        fields = '__all__'

# -------------------- Отзывы --------------------
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('text', 'stars', 'product')