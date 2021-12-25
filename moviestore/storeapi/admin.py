from django.contrib import admin
from .models import Movie, Category, Rental, Payment

# Register your models here.
admin.site.register(Movie)
admin.site.register(Category)
admin.site.register(Rental)
admin.site.register(Payment)