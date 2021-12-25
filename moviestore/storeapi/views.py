import datetime
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters, generics
from django.http import Http404
from .serializers import MovieSerializer, CategorySerializer, RentalSerializer, PaymentSerializer
from .models import Category, Movie, Rental, Payment

class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description', 'category__name')

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# View to return all movies in a category
class MovieListByCategory(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        movies = Movie.objects.filter(category=category)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

# View to return all rentals for a movie
class RentalListByMovie(APIView):
    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # only if request.user is super admin
        if request.user.is_superuser:
            movie = self.get_object(pk)
            rentals = Rental.objects.filter(movie=movie, returned_at__isnull=True)
            serializer = RentalSerializer(rentals, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # Create a new rental for a movie (only for authenticated users)
    def post(self, request, pk, format=None):
        movie = self.get_object(pk)
        if request.user.is_authenticated:
            serializer = RentalSerializer(data=request.data)
            # if serializer is valid and there is no rental for this movie by this user
            if serializer.is_valid() and not Rental.objects.filter(movie=movie, customer=request.user, returned_at__isnull=True).exists():
                serializer.save(movie=movie, customer=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

# Only super admins can view payment list
class PaymentList(APIView):
    def get_object(self, pk):
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            raise Http404

    # Only super admin can get all payments
    def get(self, request, format=None):
        if request.user.is_superuser:
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # authenticated user can post a payment on his own rentals
    def post(self, request, format=None):
        if request.user.is_authenticated:
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid():
                rental = Rental.objects.get(id=serializer.validated_data['rental'].id)
                if rental.customer == request.user:
                    amount = 0
                    if rental.rented_at.date() == datetime.datetime.now().date():
                        amount = 1
                    else:
                        days = (datetime.datetime.now().date() - rental.rented_at.date()).days
                        if days <= 3:
                            amount = days
                        else:
                            amount = 3 + (days - 3) * 0.5
                    if serializer.validated_data['amount'] == amount:
                        serializer.save(rental=rental)
                        rental.returned_at = timezone.now()
                        rental.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response({'amount': [f'amount should be equal to {amount}']}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)