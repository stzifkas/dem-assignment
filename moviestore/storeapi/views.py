import datetime
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters, generics
from django.http import Http404
from .serializers import MovieSerializer, CategorySerializer, RentalSerializer, PaymentSerializer, UserSerializer
from .models import Category, Movie, Rental, Payment

class MovieList(APIView):

    def get(self, request, format=None):
        if request.query_params:
            title = request.query_params.get('title', None)
            description = request.query_params.get('description', None)
            category = request.query_params.get('category', None)
            year = request.query_params.get('year', None)
            queryset = Movie.objects.all()
            if title:
                queryset = queryset.filter(title__icontains=title)
            if description:
                queryset = queryset.filter(description__icontains=description)
            if category:
                queryset = queryset.filter(category__name=category)
            if year:
                queryset = queryset.filter(year=year)
            serializer = MovieSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            serializer = MovieSerializer(Movie.objects.all(), many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MovieSerializer(data=request.data)
        if request.user.is_superuser:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
class MovieDetail(APIView):

    def get(self, request, pk, format=None):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        if request.user.is_superuser:
            try:
                movie = Movie.objects.get(pk=pk)
            except Movie.DoesNotExist:
                raise Http404
            serializer = MovieSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk, format=None):
        if request.user.is_superuser:
            try:
                movie = Movie.objects.get(pk=pk)
            except Movie.DoesNotExist:
                raise Http404
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class CategoryList(APIView):

    def get(self, request, format=None):
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if request.user.is_superuser:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, format=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        if request.user.is_superuser:
            try:
                category = Category.objects.get(pk=pk)
            except Category.DoesNotExist:
                raise Http404
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk, format=None):
        if request.user.is_superuser:
            try:
                category = Category.objects.get(pk=pk)
            except Category.DoesNotExist:
                raise Http404
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
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

class RentalList(APIView):
    def get(self, request,format=None):
        if request.user.is_superuser:
            if request.query_params:
                user = request.query_params.get('user', None)
                movie = request.query_params.get('movie', None)
                queryset = Rental.objects.all()
                if user:
                    queryset = queryset.filter(user__name__icontains=user)
                if movie:
                    queryset = queryset.filter(movie__title__icontains=movie)
                
                serializer = RentalSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                serializer = RentalSerializer(Rental.objects.all(), many=True)
                return Response(serializer.data)
        if request.user.is_authenticated:
            if request.query_params:
                movie = request.query_params.get('movie', None)
                queryset = Rental.objects.filter(user=request.user)
                if movie:
                    queryset = queryset.filter(movie__title__icontains=movie)
                serializer = RentalSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                serializer = RentalSerializer(Rental.objects.all(), many=True)
                return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class RentalDetail(APIView):
    
    def get(self, request, pk, format=None):
        try:
            rental = Rental.objects.get(pk=pk)
        except Rental.DoesNotExist:
            raise Http404
        if request.user.is_superuser or rental.user == request.user:
            days = (datetime.datetime.now().date() - rental.rented_at.date()).days
            if days == 0:
                rental.price = 1
            elif days <= 3:
                rental.price = days
            else:
                rental.price = 3 + (days - 3) * 0.5
            rental.save()
            rental = Rental.objects.get(pk=pk)
            serializer = RentalSerializer(rental)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk, format=None):
        try:
            rental = Rental.objects.get(pk=pk)
        except Rental.DoesNotExist:
            raise Http404
        if request.user.is_superuser or rental.user == request.user:
            rental.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class RentalListByMovie(APIView):

    def get(self, request, pk, format=None):
        movie = Movie.objects.get(pk=pk)
        if request.user.is_superuser:
            rentals = Rental.objects.filter(movie=movie)
            # for each rental calculate the price
            for rental in rentals:
                days = (datetime.datetime.now().date() - rental.rented_at.date()).days
                if days == 0:
                    rental.price = 1
                elif days <= 3:
                    rental.price = days
                else:
                    rental.price = 3 + (days - 3) * 0.5
                rental.save()
            rentals = Rental.objects.filter(movie=movie)         
            serializer = RentalSerializer(rentals, many=True)
            return Response(serializer.data)
        if request.user.is_authenticated:
            rentals = Rental.objects.filter(user=request.user, movie=movie)
            for rental in rentals:
                days = (datetime.datetime.now().date() - rental.rented_at.date()).days
                if days == 0:
                    rental.price = 1
                elif days <= 3:
                    rental.price = days
                else:
                    rental.price = 3 + (days - 3) * 0.5
                rental.save()
            rentals = Rental.objects.filter(user=request.user, movie=movie)
            serializer = RentalSerializer(rentals, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request, pk, format=None):
        if request.user.is_authenticated:
            movie = Movie.objects.get(pk=pk)
            if not Rental.objects.filter(movie=movie, user=request.user).exists():
                rental = Rental(movie=movie, user=request.user)
                rental.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class PaymentList(APIView):    
    def get(self, request, format=None):
        if request.user.is_superuser:
            if request.query_params:
                user = request.query_params.get('user', None)
                movie = request.query_params.get('movie', None)
                queryset = Payment.objects.all()
                if user:
                    queryset = queryset.filter(user__name__icontains=user)
                if movie:
                    queryset = queryset.filter(movie__title__icontains=movie)
                serializer = PaymentSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                serializer = PaymentSerializer(Payment.objects.all(), many=True)
                return Response(serializer.data)
        if request.user.is_authenticated:
            if request.query_params:
                movie = request.query_params.get('movie', None)
                queryset = Payment.objects.filter(user=request.user)
                if movie:
                    queryset = queryset.filter(movie__title__icontains=movie)
                serializer = PaymentSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                serializer = PaymentSerializer(Payment.objects.all(), many=True)
                return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class PaymentListByMovie(APIView):

    def get(self, request, pk, format=None):
        movie = Movie.objects.get(pk=pk)
        if request.user.is_superuser:
            # retrieve all payments for all rentals of the movie
            payments = Payment.objects.filter(rental__movie=movie)
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data)
        if request.user.is_authenticated:
            payments = Payment.objects.filter(rental__user=request.user, rental__movie=movie)
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request, pk, format=None):
        if request.user.is_authenticated:
            movie = Movie.objects.get(pk=pk)
            if Rental.objects.filter(movie=movie, user=request.user).exists():
                rental = Rental.objects.get(movie=movie, user=request.user)
                days = (datetime.datetime.now().date() - rental.rented_at.date()).days
                if days == 0:
                    price = 1
                elif days <= 3:
                    price = days
                else:
                    price = 3 + (days - 3) * 0.5
                rental.price = price
                rental.save()
                serializer = PaymentSerializer(data=request.data)
                if serializer.is_valid():
                    if serializer.validated_data['amount'] == price:
                        payment = Payment(rental=rental, amount=price)
                        payment.save()
                        rental.activated = True
                        rental.save()
                        return Response(status=status.HTTP_201_CREATED)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class UserList(APIView):

    def get(self, request, format=None):
        if request.user.is_superuser:
            serializer = UserSerializer(User.objects.all(), many=True)
            return Response(serializer.data)
        if request.user.is_authenticated:
            serializer = UserSerializer(User.objects.filter(pk=request.user.pk), many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):

    def get(self, request, pk, format=None):
        if request.user.is_superuser:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.user.is_authenticated:
            if request.user.pk == pk:
                user = User.objects.get(pk=pk)
                serializer = UserSerializer(user)
                return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request, pk, format=None):
        if request.user.is_superuser:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_authenticated:
            if request.user.pk == pk:
                user = User.objects.get(pk=pk)
                serializer = UserSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk, format=None):
        if request.user.is_superuser:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.user.is_authenticated:
            if request.user.pk == pk:
                user = User.objects.get(pk=pk)
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)