from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('movies/', views.MovieList.as_view()),
    path('movies/<int:pk>/', views.MovieDetail.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:pk>/', views.CategoryDetail.as_view()),
    path('categories/<int:pk>/movies/', views.MovieListByCategory.as_view()),
    path('rentals/', views.RentalList.as_view()),
    path('rentals/<int:pk>/', views.RentalDetail.as_view()),
    path('movies/<int:pk>/rentals/', views.RentalListByMovie.as_view()),
    path('payments/', views.PaymentList.as_view()),
    path('movies/<int:pk>/payments/', views.PaymentListByMovie.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]