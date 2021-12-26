import datetime
from django.test import TestCase, testcases
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from .models import Movie, Category, Rental, Payment
from . import views

# Create your tests here.
class MovieListTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        adventure_category = Category.objects.create(name='Adventure')
        fantasy_category = Category.objects.create(name='Fantasy')
        movie1 = Movie.objects.create(title='Harry Potter', description='', year=2001, imdb_rating=7.5)
        movie2 = Movie.objects.create(title='Lego Movie', description='', year=2014, imdb_rating=7.5)
        movie1.category.set([adventure_category, fantasy_category])
        movie2.category.set([adventure_category])

    def test_movie_list(self):
        request = self.factory.get('/movies/')
        response = views.MovieList.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()

class MovieListTest2(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        drama_category = Category.objects.create(name='Drama')
        crime_category = Category.objects.create(name='Crime')
        movie1 = Movie.objects.create(title='The Godfather', description='The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.', year=1972, imdb_rating=9.2)
        movie2 = Movie.objects.create(title='The Godfather: Part II', description='The early life and career of Vito Corleone in 1920s New York is portrayed while his son, Michael, expands and tightens his grip on the family crime syndicate.', year=1974, imdb_rating=9.0)
        movie1.category.set([crime_category])
        movie2.category.set([drama_category])

    def test_movie_list_with_category(self):
        request = self.factory.get('/movies/?category=Crime')
        response = views.MovieList.as_view()(request)
        self.assertEqual(len(response.data), 1)
    
    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()

class MovieListTest3(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        category1 = Category.objects.create(name='Adventure')
        category2 = Category.objects.create(name='Fantasy')
        movie1 = Movie.objects.create(title='The Lord of the Rings: The Fellowship of the Ring', description='A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.', year=2001, imdb_rating=8.8)
        movie2 = Movie.objects.create(title='The Lord of the Rings: The Two Towers', description='While Frodo and Sam edge closer to Mordor with the help of the shifty Gollum, the divided fellowship makes a stand against Sauron\'s new ally, Saruman, and his hordes of Isengard.', year=2002, imdb_rating=8.8)
        movie1.category.set([category1])
        movie2.category.set([category2])

    def test_movie_list_with_category_and_year(self):
        request = self.factory.get('/movies/?category=Adventure&year=2001')
        response = views.MovieList.as_view()(request)
        self.assertEqual(len(response.data), 1)

    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()

class MovieListTest4(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        category1 = Category.objects.create(name='Adventure')
        User.objects.create_superuser(username='admin', password='admin')
    
    def test_movie_creation(self):
        user = User.objects.get(username='admin')
        category = Category.objects.get(name='Adventure')
        request = self.factory.post('/movies/', {'title': 'Tomb Raider', 'description': 'A Lara Croft film', 'year': 2018, 'imdb_rating': 7.5, 'category': [category.id]}, format='json')
        force_authenticate(request, user=user)
        response = views.MovieList.as_view()(request)
        self.assertEqual(response.status_code, 201)

class MovieDetailTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        adventure_category = Category.objects.create(name='Adventure')
        fantasy_category = Category.objects.create(name='Fantasy')
        movie1 = Movie.objects.create(title='Harry Potter', description='', year=2001, imdb_rating=7.5)
        movie2 = Movie.objects.create(title='Lego Movie', description='', year=2014, imdb_rating=7.5)
        movie1.category.set([adventure_category])
        movie2.category.set([fantasy_category])

    def test_movie_detail(self):
        request = self.factory.get('/movies/1/')
        response = views.MovieDetail.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()

class MovieDetailTest2(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        drama_category = Category.objects.create(name='Drama')
        crime_category = Category.objects.create(name='Crime')
        movie1 = Movie.objects.create(title='The Godfather', description='The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.', year=1972, imdb_rating=9.2)
        movie2 = Movie.objects.create(title='The Godfather: Part II', description='The early life and career of Vito Corleone in 1920s New York is portrayed while his son, Michael, expands and tightens his grip on the family crime syndicate.', year=1974, imdb_rating=9.0)
        movie1.category.set([crime_category])
        movie2.category.set([drama_category])

    def test_movie_detail_with_title(self):
        movie = Movie.objects.get(title='The Godfather')
        request = self.factory.get(f'/movies/{movie.id}')
        response = views.MovieDetail.as_view()(request, pk=movie.id)
        self.assertEqual(response.data['title'],'The Godfather')
    
    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()

class MovieDetailTest3(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        category1 = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category1])
        self.user = User.objects.create_superuser(username='admin', password='admin')
    
    def test_movie_edit(self):
        movie = Movie.objects.get(title='Tomb Raider')
        category = Category.objects.get(name='Adventure')
        request = self.factory.put(f'/movies/{movie.id}', {'title': 'Tomb Raider 1', 'description': 'A Lara Croft film', 'year': 2018, 'imdb_rating': 7.5, 'category': [category.id]}, format='json')
        force_authenticate(request, user=self.user)
        response = views.MovieDetail.as_view()(request, pk=movie.id)
        self.assertEqual(response.data['title'],'Tomb Raider 1')

class CategoryListTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        Category.objects.create(name='Adventure')
        Category.objects.create(name='Fantasy')
    
    def test_category_list(self):
        request = self.factory.get('/categories/')
        response = views.CategoryList.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        Category.objects.all().delete()

class CategoryListTest2(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        Category.objects.create(name='Drama')
        Category.objects.create(name='Crime')
    
    def test_category_list_with_year(self):
        request = self.factory.get('/categories/')
        response = views.CategoryList.as_view()(request)
        self.assertEqual(len(response.data), 2)
    
    def tearDown(self):
        Category.objects.all().delete()

class CategoryListTest3(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_superuser(username='admin', password='admin')
    
    def test_category_creation(self):
        request = self.factory.post('/categories/', {'name': 'Adventure'}, format='json')
        force_authenticate(request, user=self.user)
        response = views.CategoryList.as_view()(request)
        self.assertEqual(response.status_code, 201)
    
    def tearDown(self):
        Category.objects.all().delete()

class CategoryDetailTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        Category.objects.create(name='Adventure')
    
    def test_category_detail(self):
        category = Category.objects.get(name='Adventure')
        request = self.factory.get(f'/categories/{category.id}/')
        response = views.CategoryDetail.as_view()(request, pk=category.id)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        Category.objects.all().delete()

class CategoryDetailTest2(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        Category.objects.create(name='Comedy')
        self.user = User.objects.create_superuser(username='admin', password='admin')
    
    def test_category_edit(self):
        category = Category.objects.get(name='Comedy')
        request = self.factory.put(f'/categories/{category.id}', {'name': 'Adventure'}, format='json')
        force_authenticate(request, user=self.user)
        response = views.CategoryDetail.as_view()(request, pk=category.id)
        self.assertEqual(response.data['name'],'Adventure')
    
    def tearDown(self):
        Category.objects.all().delete()

class CategoryDetailTest3(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_superuser(username='admin', password='admin')
    
    def test_category_deletion(self):
        category = Category.objects.create(name='Adventure')
        request = self.factory.delete(f'/categories/{category.id}/')
        force_authenticate(request, user=self.user)
        response = views.CategoryDetail.as_view()(request, pk=category.id)
        self.assertEqual(response.status_code, 204)

class MovieListByCategoryTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        category = Category.objects.create(name='Adventure')
        movie1 = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie2 = Movie.objects.create(title='Tomb Raider 2', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie1.category.set([category])
        movie2.category.set([category])

    def test_movie_list_by_category(self):
        category = Category.objects.get(name='Adventure')
        request = self.factory.get(f'/categories/{category.id}/movies/')
        response = views.MovieListByCategory.as_view()(request, pk=category.id)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        Category.objects.all().delete()
        Movie.objects.all().delete()

class MovieListByCategoryTest2(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        category = Category.objects.create(name='Adventure')
        movie1 = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie2 = Movie.objects.create(title='Tomb Raider 2', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie1.category.set([category])
        movie2.category.set([category])

    def test_movie_list_by_category(self):
        category = Category.objects.get(name='Adventure')
        request = self.factory.get(f'/categories/{category.id}/movies/')
        response = views.MovieListByCategory.as_view()(request, pk=category.id)
        self.assertEqual(len(response.data), 2)
    
    def tearDown(self):
        Category.objects.all().delete()
        Movie.objects.all().delete()

class RentalListTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        Rental.objects.create(user=user, movie=movie)
    
    def test_rental_list(self):
        request = self.factory.get('/rentals/')
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.RentalList.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        Rental.objects.all().delete()

class RentalListTest2(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        Rental.objects.create(user=user, movie=movie)
    
    def test_rental_list_with_user(self):
        request = self.factory.get('/rentals/')
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.RentalList.as_view()(request)
        self.assertEqual(len(response.data), 1)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class RentalListTest3(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        Rental.objects.create(user=user, movie=movie)
    
    def test_rental_list_unauthorized(self):
        request = self.factory.get('/rentals/')
        response = views.RentalList.as_view()(request)
        self.assertEqual(response.status_code, 401)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class RentalListTest4(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user1 = User.objects.create_user(username='user1', password='user1')
        user2 = User.objects.create_user(username='user2', password='user2')
        user3 = User.objects.create_user(username='user3', password='user3')
        user4 = User.objects.create_superuser(username='admin', password='admin')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        Rental.objects.create(user=user1, movie=movie)
        Rental.objects.create(user=user2, movie=movie)
    
    def test_rental_list_superuser(self):
        request = self.factory.get('/rentals/')
        user = User.objects.get(username='admin')
        force_authenticate(request, user=user)
        response = views.RentalList.as_view()(request)
        self.assertEqual(len(response.data), 2)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class RentalListTest5(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])

    def test_rental_creation(self):
        movie = Movie.objects.get(title='Tomb Raider')
        user = User.objects.get(username='user1')
        request = self.factory.post(f'/movies/{movie.id}/rentals/', {})
        force_authenticate(request, user=user)
        response = views.RentalListByMovie.as_view()(request, pk=movie.id)
        self.assertEqual(response.status_code, 201)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class RentalListTest6(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
    
    def test_rental_creation_unauthorized(self):
        movie = Movie.objects.get(title='Tomb Raider')
        request = self.factory.post(f'/movies/{movie.id}/rentals/', {})
        response = views.RentalListByMovie.as_view()(request, pk=movie.id)
        self.assertEqual(response.status_code, 401)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class RentalDetailTest1(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        Rental.objects.create(user=user, movie=movie)
    
    def test_rental_detail(self):
        rental = Rental.objects.get(user__username='user1')
        request = self.factory.get(f'/rentals/{rental.id}/')
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.RentalDetail.as_view()(request, pk=rental.id)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class RentalDetailTest2(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        Rental.objects.create(user=user, movie=movie)
    
    def test_rental_detail_unauthorized(self):
        rental = Rental.objects.get(user__username='user1')
        request = self.factory.get(f'/rentals/{rental.id}/')
        response = views.RentalDetail.as_view()(request, pk=rental.id)
        self.assertEqual(response.status_code, 401)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class RentalDetailTest3(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        Rental.objects.create(user=user, movie=movie)
    
    def test_rental_delete(self):
        rental = Rental.objects.get(user__username='user1')
        request = self.factory.delete(f'/rentals/{rental.id}/')
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.RentalDetail.as_view()(request, pk=rental.id)
        self.assertEqual(response.status_code, 204)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class RentalDetailTest4(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        date = datetime.datetime.now() - datetime.timedelta(days=5) + datetime.timedelta(hours=1)
        Rental.objects.create(user=user, movie=movie, rented_at=date)
    
    def test_rental_price(self):
        rental = Rental.objects.get(user__username='user1')
        request = self.factory.get(f'/rentals/{rental.id}/price/')
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.RentalDetail.as_view()(request, pk=rental.id)
        self.assertEqual(response.data['price'], 4)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class RentalDetailTest5(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        date = datetime.datetime.now() - datetime.timedelta(days=3)
        Rental.objects.create(user=user, movie=movie, rented_at=date)
    
    def test_rental_price(self):
        rental = Rental.objects.get(user__username='user1')
        request = self.factory.get(f'/rentals/{rental.id}/price/')
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.RentalDetail.as_view()(request, pk=rental.id)
        self.assertEqual(response.data['price'], 3)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class RentalDetailTest6(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        Rental.objects.create(user=user, movie=movie)
    
    def test_rental_price(self):
        rental = Rental.objects.get(user__username='user1')
        request = self.factory.get(f'/rentals/{rental.id}/price/')
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.RentalDetail.as_view()(request, pk=rental.id)
        self.assertEqual(response.data['price'], 1)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class PaymentListTest1(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        rental = Rental.objects.create(user=user, movie=movie)
        Payment.objects.create(amount=4, rental = rental)

    def test_payment_list_unauthorized(self):
        request = self.factory.get('/payments/')
        response = views.PaymentList.as_view()(request)
        self.assertEqual(response.status_code, 401)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class PaymentListTest2(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        rental = Rental.objects.create(user=user, movie=movie)
        Payment.objects.create(amount=4, rental = rental)
    
    def test_payment_list_authorized(self):
        request = self.factory.get('/payments/')
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.PaymentList.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class PaymentListTest3(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        rental = Rental.objects.create(user=user, movie=movie)
        Payment.objects.create(amount=4, rental = rental)
    
    def test_payment_list_authorized(self):
        request = self.factory.get('/payments/')
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.PaymentList.as_view()(request)
        self.assertEqual(len(response.data), 1)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class PaymentListTest4(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        Rental.objects.create(user=user, movie=movie)
        user2 = User.objects.create_user(username='user2', password='user2')
        category2 = Category.objects.create(name='Action')
        movie2 = Movie.objects.create(title='Tomb Raider 2', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie2.category.set([category2])
        rental1 = Rental.objects.create(user=user2, movie=movie2)
        rental2 = Rental.objects.create(user=user2, movie=movie)
        Payment.objects.create(amount=4, rental = rental1)
        Payment.objects.create(amount=4, rental = rental2)
        superuser = User.objects.create_superuser(username='superuser', password='superuser')

    def test_payment_list_superuser(self):
        request = self.factory.get('/payments/')
        user = User.objects.get(username='superuser')
        force_authenticate(request, user=user)
        response = views.PaymentList.as_view()(request)
        self.assertEqual(len(response.data), 2)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class PaymentListByMovieTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        Rental.objects.create(user=user, movie=movie)
        user2 = User.objects.create_user(username='user2', password='user2')
        category2 = Category.objects.create(name='Action')
        movie2 = Movie.objects.create(title='Tomb Raider 2', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie2.category.set([category2])
        rental1 = Rental.objects.create(user=user2, movie=movie2)
        rental2 = Rental.objects.create(user=user2, movie=movie)
        Payment.objects.create(amount=4, rental = rental1)
        Payment.objects.create(amount=4, rental = rental2)
        superuser = User.objects.create_superuser(username='superuser', password='superuser')

    def test_payment_list_by_movie_superuser(self):
        movie = Movie.objects.get(title='Tomb Raider 2')
        request = self.factory.get(f'/movies/{movie.id}/payments/')
        user = User.objects.get(username='superuser')
        force_authenticate(request, user=user)
        response = views.PaymentListByMovie.as_view()(request, pk=movie.id)
        self.assertEqual(len(response.data), 1)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class PaymentListByMovieTest2(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        Rental.objects.create(user=user, movie=movie)
        user2 = User.objects.create_user(username='user2', password='user2')
        category2 = Category.objects.create(name='Action')
        movie2 = Movie.objects.create(title='Tomb Raider 2', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie2.category.set([category2])
        rental1 = Rental.objects.create(user=user, movie=movie)
        rental2 = Rental.objects.create(user=user2, movie=movie)
        Payment.objects.create(amount=4, rental = rental1)
        Payment.objects.create(amount=4, rental = rental2)

    def test_payment_list_by_movie_user(self):
        movie = Movie.objects.get(title='Tomb Raider')
        request = self.factory.get(f'/movies/{movie.id}/payments/')
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.PaymentListByMovie.as_view()(request, pk=movie.id)
        self.assertEqual(len(response.data), 1)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class PaymentListByMovieTest3(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        Rental.objects.create(user=user, movie=movie)
        user2 = User.objects.create_user(username='user2', password='user2')
        category2 = Category.objects.create(name='Action')
        movie2 = Movie.objects.create(title='Tomb Raider 2', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie2.category.set([category2])
        rental1 = Rental.objects.create(user=user, movie=movie)
        rental2 = Rental.objects.create(user=user2, movie=movie)
        Payment.objects.create(amount=4, rental = rental1)
        Payment.objects.create(amount=4, rental = rental2)

    def test_payment_list_by_movie_user_not_authenticated(self):
        movie = Movie.objects.get(title='Tomb Raider 2')
        request = self.factory.get(f'/movies/{movie.id}/payments/')
        response = views.PaymentListByMovie.as_view()(request, pk=movie.id)
        self.assertEqual(response.status_code, 401)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class PaymentListByMovieTest4(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        category2 = Category.objects.create(name='Action')
        movie2 = Movie.objects.create(title='Tomb Raider 2', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie2.category.set([category2])
        Rental.objects.create(user=user, movie=movie)
    
    def test_payment_list_by_movie_create(self):
        movie = Movie.objects.get(title='Tomb Raider')
        request = self.factory.post(f'/movies/{movie.id}/payments/', {'amount': 1})
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.PaymentListByMovie.as_view()(request, pk=movie.id)
        self.assertEqual(response.status_code, 201)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class PaymentListByMovieTest5(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(username='user1', password='user1')
        category = Category.objects.create(name='Adventure')
        movie = Movie.objects.create(title='Tomb Raider', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie.category.set([category])
        category2 = Category.objects.create(name='Action')
        movie2 = Movie.objects.create(title='Tomb Raider 2', description='A Lara Croft film', year=2018, imdb_rating=7.5)
        movie2.category.set([category2])
        Rental.objects.create(user=user, movie=movie)
    
    def test_payment_list_by_movie_create(self):
        movie = Movie.objects.get(title='Tomb Raider')
        request = self.factory.post(f'/movies/{movie.id}/payments/', {'amount': 10})
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.PaymentListByMovie.as_view()(request, pk=movie.id)
        self.assertEqual(response.status_code, 400)
    
    def tearDown(self):
        Rental.objects.all().delete()
        Movie.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()

class UserListTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.create_user(username='user1', password='user1')
        User.objects.create_user(username='user2', password='user2')
        User.objects.create_user(username='user3', password='user3')
        User.objects.create_superuser(username='admin', password='admin')
    
    def test_user_list_get_unauthorized(self):
        request = self.factory.get('/users/')
        response = views.UserList.as_view()(request)
        self.assertEqual(response.status_code, 401)
    
    def tearDown(self): 
        User.objects.all().delete()

class UserListTest2(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.create_user(username='user1', password='user1')
        User.objects.create_user(username='user2', password='user2')
        User.objects.create_user(username='user3', password='user3')
        User.objects.create_superuser(username='admin', password='admin')
    
    def test_user_list_get_superuser(self):
        request = self.factory.get('/users/')
        user = User.objects.get(username='admin')
        force_authenticate(request, user=user)
        response = views.UserList.as_view()(request)
        self.assertEqual(len(response.data), 4)
    
    def tearDown(self): 
        User.objects.all().delete()

class UserListTest3(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.create_user(username='user1', password='user1')
        User.objects.create_user(username='user2', password='user2')
        User.objects.create_user(username='user3', password='user3')
        User.objects.create_superuser(username='admin', password='admin')
    
    def test_user_list_get_user(self):
        request = self.factory.get('/users/')
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.UserList.as_view()(request)
        self.assertEqual(len(response.data), 1)
    
    def tearDown(self): 
        User.objects.all().delete()

class UserListTest4(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.create_user(username='user1', password='user1')
        User.objects.create_user(username='user2', password='user2')
        User.objects.create_user(username='user3', password='user3')
        User.objects.create_superuser(username='admin', password='admin')
    
    def test_user_list_post_unauthorized(self):
        request = self.factory.post('/users/', {'username': 'user4', 'password': 'user4'})
        response = views.UserList.as_view()(request)
        self.assertEqual(response.status_code, 201)
    
    def tearDown(self): 
        User.objects.all().delete()

class UserDetailTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.create_user(username='user1', password='user1')
        User.objects.create_user(username='user2', password='user2')
        User.objects.create_user(username='user3', password='user3')
        User.objects.create_superuser(username='admin', password='admin')
    
    def test_user_detail_get_unauthorized(self):
        user = User.objects.get(username='user1')
        request = self.factory.get(f'/users/{user.id}/')
        response = views.UserDetail.as_view()(request, pk=user.id)
        self.assertEqual(response.status_code, 401)
    
    def test_user_detail_get_superuser(self):
        user = User.objects.get(username='user1')
        request = self.factory.get(f'/users/{user.id}/')
        user = User.objects.get(username='admin')
        force_authenticate(request, user=user)
        response = views.UserDetail.as_view()(request, pk=user.id)
        self.assertEqual(response.status_code, 200)
    
    def test_user_detail_get_user(self):
        user = User.objects.get(username='user1')
        request = self.factory.get(f'/users/{user.id}/')
        user = User.objects.get(username='user1')
        force_authenticate(request, user=user)
        response = views.UserDetail.as_view()(request, pk=user.id)
        self.assertEqual(response.status_code, 200)
    
    def test_user_detail_put_unauthorized(self):
        user = User.objects.get(username='user1')
        request = self.factory.put(f'/users/{user.id}/', {'username': 'user4'})
        response = views.UserDetail.as_view()(request, pk=user.id)
        self.assertEqual(response.status_code, 401)
    
    def test_user_detail_put_superuser(self):
        user1 = User.objects.get(username='user1')
        request = self.factory.put(f'/users/{user1.id}/', {'username': 'user1', 'password': 'user4'})
        user2 = User.objects.get(username='admin')
        force_authenticate(request, user=user2)
        response = views.UserDetail.as_view()(request, pk=user1.id)
        self.assertEqual(response.status_code, 200)
    
    def test_user_detail_put_user(self):
        user = User.objects.get(username='user1')
        request = self.factory.put(f'/users/{user.id}/', {'username': 'user1', 'password': 'user4'})
        force_authenticate(request, user=user)
        response = views.UserDetail.as_view()(request, pk=user.id)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self): 
        User.objects.all().delete()