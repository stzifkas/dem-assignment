from rest_framework import serializers
from .models import Movie, Category, Rental, Payment

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # serialize id, title, description, year, imdb_rating and category name
        fields = ('id', 'title', 'description', 'year', 'imdb_rating', 'category')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ('id', 'rented_at', 'returned_at')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'rental', 'amount','created_at', 'updated_at')