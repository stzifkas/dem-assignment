from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Category, Rental, Payment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
class MovieSerializer(serializers.ModelSerializer):
    # serialize category name instead of category id
    # category = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'year', 'imdb_rating', 'category')


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ('id', 'rented_at', 'activated', 'price')

class PaymentSerializer(serializers.ModelSerializer):
    rental = RentalSerializer(many=False, read_only=True)
    class Meta:
        model = Payment
        fields = ('id', 'rental', 'amount','created_at', 'updated_at')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')