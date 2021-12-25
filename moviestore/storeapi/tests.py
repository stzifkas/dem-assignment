import datetime
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from .models import Movie, Category, Rental, Payment
from . import views

# Create your tests here.
# test the MovieList endpoint
class MovieListTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # create a category
        category = Category.objects.create(name='Action')
        # create a few movies
        Movie.objects.create(title='The Matrix', description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', year=1999, imdb_rating=8.7, category=category)

    def test_movie_list(self):
        # create a request
        request = self.factory.get('/movies/')
        # call the endpoint
        response = views.MovieList.as_view()(request)
        # check the response
        self.assertEqual(response.status_code, 200)
    
    # tear down the test data
    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()

# test the MovieDetail endpoint
class MovieDetailTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # create a category
        category = Category.objects.create(name='Action')
        # create a few movies
        Movie.objects.create(title='The Matrix', description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', year=1999, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Reloaded', description='Neo has spent two years in the past looking for the one thing that he knows will bring him back to the present.', year=2003, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Revolutions', description='The human city of Zion defends itself against the massive invasion of the machines as Neo fights to end the war at another front while also opposing the rogue Agent Smith.', year=2003, imdb_rating=8.7, category=category)

    def test_movie_detail(self):
        # create a request
        request = self.factory.get('/movies/1/')
        # call the endpoint
        response = views.MovieDetail.as_view()(request, pk=1)
        # check the response
        self.assertEqual(response.status_code, 200)
    
    # tear down the test data
    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()

# test the CategoryList endpoint
class CategoryListTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # create a few categories
        Category.objects.create(name='Action')
        Category.objects.create(name='Comedy')
        Category.objects.create(name='Drama')
        # create a few movies in each category
        category = Category.objects.get(name='Action')
        Movie.objects.create(title='The Matrix', description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', year=1999, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Reloaded', description='Neo has spent two years in the past looking for the one thing that he knows will bring him back to the present.', year=2003, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Revolutions', description='The human city of Zion defends itself against the massive invasion of the machines as Neo fights to end the war at another front while also opposing the rogue Agent Smith.', year=2003, imdb_rating=8.7, category=category)
        category = Category.objects.get(name='Comedy')
        Movie.objects.create(title='The Hangover', description='Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing. They make their way around the city in order to find their friend before his wedding.', year=2009, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Hangover Part II', description='While trying to recover from a bachelor party at a strip club, a Hangover-induced hangover kills Mike, and his friend Darryl finds himself dragged into the world of drugs and alcohol after he overdoses.', year=2011, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Hangover Part III', description='While trying to recover from a bachelor party at a strip club, a Hangover-induced hangover kills Mike, and his friend Darryl finds himself dragged into the world of drugs and alcohol after he overdoses.', year=2013, imdb_rating=8.7, category=category)
        category = Category.objects.get(name='Drama')
        Movie.objects.create(title='The Dark Knight', description='When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, the caped crusader must come to terms with one of the greatest psychological tests of his ability to fight injustice.', year=2008, imdb_rating=8.7, category=category)

    def test_category_list(self):
        # create a request
        request = self.factory.get('/categories/')
        # call the endpoint
        response = views.CategoryList.as_view()(request)
        # check the response
        self.assertEqual(response.status_code, 200)
    
    # tear down the test data
    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()

# test the CategoryDetail endpoint
class CategoryDetailTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # create a few categories
        Category.objects.create(name='Action')
        Category.objects.create(name='Comedy')
        Category.objects.create(name='Drama')
        # create a few movies in each category
        category = Category.objects.get(name='Action')
        Movie.objects.create(title='The Matrix', description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', year=1999, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Reloaded', description='Neo has spent two years in the past looking for the one thing that he knows will bring him back to the present.', year=2003, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Revolutions', description='The human city of Zion defends itself against the massive invasion of the machines as Neo fights to end the war at another front while also opposing the rogue Agent Smith.', year=2003, imdb_rating=8.7, category=category)
        category = Category.objects.get(name='Comedy')
        Movie.objects.create(title='The Hangover', description='Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing. They make their way around the city in order to find their friend before his wedding.', year=2009, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Hangover Part II', description='While trying to recover from a bachelor party at a strip club, a Hangover-induced hangover kills Mike, and his friend Darryl finds himself dragged into the world of drugs and alcohol after he overdoses.', year=2011, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Hangover Part III', description='While trying to recover from a bachelor party at a strip club, a Hangover-induced hangover kills Mike, and his friend Darryl finds himself dragged into the world of drugs and alcohol after he overdoses.', year=2013, imdb_rating=8.7, category=category)
        category = Category.objects.get(name='Drama')
        Movie.objects.create(title='The Dark Knight', description='When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, the caped crusader must come to terms with one of the greatest psychological tests of his ability to fight injustice.', year=2008, imdb_rating=8.7, category=category)
        
    def test_category_detail(self):
        # create a request
        request = self.factory.get('/categories/1/')
        # call the endpoint
        response = views.CategoryDetail.as_view()(request, pk=1)
        # check the response
        self.assertEqual(response.status_code, 200)
    
    # tear down the test data
    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()

# test the MovieListByCategory endpoint
class MovieListByCategoryTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # create a few categories
        Category.objects.create(name='Action')
        Category.objects.create(name='Comedy')
        Category.objects.create(name='Drama')
        # create a few movies in each category
        category = Category.objects.get(name='Action')
        Movie.objects.create(title='The Matrix', description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', year=1999, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Reloaded', description='Neo has spent two years in the past looking for the one thing that he knows will bring him back to the present.', year=2003, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Revolutions', description='The human city of Zion defends itself against the massive invasion of the machines as Neo fights to end the war at another front while also opposing the rogue Agent Smith.', year=2003, imdb_rating=8.7, category=category)
        category = Category.objects.get(name='Comedy')
        Movie.objects.create(title='The Hangover', description='Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing. They make their way around the city in order to find their friend before his wedding.', year=2009, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Hangover Part II', description='While trying to recover from a bachelor party at a strip club, a Hangover-induced hangover kills Mike, and his friend Darryl finds himself dragged into the world of drugs and alcohol after he overdoses.', year=2011, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Hangover Part III', description='While trying to recover from a bachelor party at a strip club, a Hangover-induced hangover kills Mike, and his friend Darryl finds himself dragged into the world of drugs and alcohol after he overdoses.', year=2013, imdb_rating=8.7, category=category)
        category = Category.objects.get(name='Drama')
        Movie.objects.create(title='The Dark Knight', description='When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, the caped crusader must come to terms with one of the greatest psychological tests of his ability to fight injustice.', year=2008, imdb_rating=8.7, category=category)

    def test_movie_list_by_category(self):
        # create a request
        request = self.factory.get('/categories/1/movies/')
        # call the endpoint
        response = views.MovieListByCategory.as_view()(request, pk=1)
        # check the response
        self.assertEqual(response.status_code, 200)
    
    # tear down the test data
    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()

# test the RentalListByMovie endpoint
class RentalListByMovieTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # create a few categories
        Category.objects.create(name='Action')
        Category.objects.create(name='Comedy')
        Category.objects.create(name='Drama')
        # create a few movies in each category
        category = Category.objects.get(name='Action')
        Movie.objects.create(title='The Matrix', description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', year=1999, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Reloaded', description='Neo has spent two years in the past looking for the one thing that he knows will bring him back to the present.', year=2003, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Revolutions', description='The human city of Zion defends itself against the massive invasion of the machines as Neo fights to end the war at another front while also opposing the rogue Agent Smith.', year=2003, imdb_rating=8.7, category=category)
        category = Category.objects.get(name='Comedy')
        Movie.objects.create(title='The Hangover', description='Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing. They make their way around the city in order to find their friend before his wedding.', year=2009, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Hangover Part II', description='While trying to recover from a bachelor party at a strip club, a Hangover-induced hangover kills Mike, and his friend Darryl finds himself dragged into the world of drugs and alcohol after he overdoses.', year=2011, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Hangover Part III', description='While trying to recover from a bachelor party at a strip club, a Hangover-induced hangover kills Mike, and his friend Darryl finds himself dragged into the world of drugs and alcohol after he overdoses.', year=2013, imdb_rating=8.7, category=category)
        category = Category.objects.get(name='Drama')
        Movie.objects.create(title='The Dark Knight', description='When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, the caped crusader must come to terms with one of the greatest psychological tests of his ability to fight injustice.', year=2008, imdb_rating=8.7, category=category)
        # create a few django users
        User.objects.create_user(username='user1', password='user1')
        User.objects.create_user(username='user2', password='user2')
        User.objects.create_user(username='user3', password='user3')
        # create a few rentals for each user
        user = User.objects.get(username='user1')
        movie = Movie.objects.get(title='The Matrix')
        Rental.objects.create(customer=user, movie=movie, rented_at=datetime.date.today())
        user = User.objects.get(username='user2')
        movie = Movie.objects.get(title='The Matrix')
        Rental.objects.create(customer=user, movie=movie, rented_at=datetime.date.today())
        user = User.objects.get(username='user3')
        movie = Movie.objects.get(title='The Matrix')
        Rental.objects.create(customer=user, movie=movie, rented_at=datetime.date.today())
        # create a superuser
        User.objects.create_superuser(username='admin', password='admin')

    def test_rental_list_by_movie(self):
        # get 'The Matrix' id from the database
        movie = Movie.objects.get(title='The Matrix')
        id = movie.id      
        # create a request
        request = self.factory.get(f'/movies/{id}/rentals/')
        # authenticate the request as admin
        force_authenticate(request, user=User.objects.get(username='admin'))
        # call the endpoint
        response = views.RentalListByMovie.as_view()(request, pk=1)
        # check the response
        self.assertEqual(response.status_code, 200)
    
    # tear down the test data
    def tearDown(self):
        Movie.objects.all().delete()
        User.objects.all().delete()
        Rental.objects.all().delete()

# test the PaymentList endpoint
class PaymentListTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # create a few categories
        Category.objects.create(name='Action')
        Category.objects.create(name='Comedy')
        # create a few movies in each category
        category = Category.objects.get(name='Action')
        Movie.objects.create(title='The Matrix', description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', year=1999, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Reloaded', description='Neo has spent two years in the past looking for the one thing that he knows will bring him back to the present.', year=2003, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Revolutions', description='The human city of Zion defends itself against the massive invasion of the machines as Neo fights to end the war at another front while also opposing the rogue Agent Smith.', year=2003, imdb_rating=8.7, category=category)
        # create a few django users
        User.objects.create_user(username='user1', password='user1')
        User.objects.create_user(username='user2', password='user2')
        User.objects.create_user(username='user3', password='user3')
        # create a few rentals for each user with returned_at set
        user = User.objects.get(username='user1')
        movie = Movie.objects.get(title='The Matrix')
        Rental.objects.create(customer=user, movie=movie, rented_at=datetime.datetime.now(), returned_at=timezone.now())
        user = User.objects.get(username='user2')
        movie = Movie.objects.get(title='The Matrix')
        Rental.objects.create(customer=user, movie=movie, rented_at=datetime.datetime.now(), returned_at=timezone.now())
        user = User.objects.get(username='user3')
        movie = Movie.objects.get(title='The Matrix')
        Rental.objects.create(customer=user, movie=movie, rented_at=datetime.datetime.now(), returned_at=timezone.now())
        # create a payment object for each rental
        user = User.objects.get(username='user1')
        rental = Rental.objects.get(customer=user, movie=movie)
        Payment.objects.create(rental=rental, amount=10.0, created_at=datetime.date.today())
        user = User.objects.get(username='user2')
        rental = Rental.objects.get(customer=user, movie=movie)
        Payment.objects.create(rental=rental, amount=10.0, created_at=datetime.date.today())
        user = User.objects.get(username='user3')
        rental = Rental.objects.get(customer=user, movie=movie)
        Payment.objects.create(rental=rental, amount=10.0, created_at=datetime.date.today())
        # create a superuser
        User.objects.create_superuser(username='admin', password='admin')

    def test_payment_list(self):
        # create a request
        request = self.factory.get('/payments/')
        # authenticate the request as admin
        force_authenticate(request, user=User.objects.get(username='admin'))
        # call the endpoint
        response = views.PaymentList.as_view()(request)
        # check the response
        self.assertEqual(response.status_code, 200)
    
    # tear down the test data
    def tearDown(self):
        Movie.objects.all().delete()
        User.objects.all().delete()
        Rental.objects.all().delete()
        Payment.objects.all().delete()

# test new rental for a movie
class RentalTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # create a few categories
        Category.objects.create(name='Action')
        Category.objects.create(name='Comedy')
        # create a few movies in each category
        category = Category.objects.get(name='Action')
        Movie.objects.create(title='The Matrix', description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', year=1999, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Reloaded', description='Neo has spent two years in the past looking for the one thing that he knows will bring him back to the present.', year=2003, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Revolutions', description='The human city of Zion defends itself against the massive invasion of the machines as Neo fights to end the war at another front while also opposing the rogue Agent Smith.', year=2003, imdb_rating=8.7, category=category)
        # create a few django users
        User.objects.create_user(username='user1', password='user1')
        User.objects.create_user(username='user2', password='user2')
        User.objects.create_user(username='user3', password='user3')
        # create a super user
        User.objects.create_superuser(username='admin', password='admin')

    def test_rental(self):
        # get 'The Matrix' id from the database
        movie = Movie.objects.get(title='The Matrix')
        id = movie.id
        # authenticate user1
        user = User.objects.get(username='user1')
        # create an empty post request for the rental
        request = self.factory.post(f'/movies/{id}/rentals/')
        force_authenticate(request, user=user)
        # call the endpoint
        response = views.RentalListByMovie.as_view()(request, pk=id)
        # check the response
        self.assertEqual(response.status_code, 201)

    # tear down the test data
    def tearDown(self):
        Movie.objects.all().delete()
        User.objects.all().delete()
        Rental.objects.all().delete()

# test new movie with full data
class MovieTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # create a few categories
        Category.objects.create(name='Action')
        Category.objects.create(name='Comedy')
        # create a few movies in each category
        category = Category.objects.get(name='Action')
        Movie.objects.create(title='The Matrix', description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', year=1999, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Reloaded', description='Neo has spent two years in the past looking for the one thing that he knows will bring him back to the present.', year=2003, imdb_rating=8.7, category=category)
        # create a superuser
        User.objects.create_superuser(username='admin', password='admin')

    def test_movie(self):
        # authenticate as admin
        user = User.objects.get(username='admin')
        # grab 'Comedy' id from the database
        category = Category.objects.get(name='Comedy')
        id = category.id
        # create a post request for the movie 'Hangover'
        request = self.factory.post('/movies/', {'title': 'Hangover', 'description': 'A guy goes to a party and gets drunk, but the bartender tells him to stop and says he has to get out of the bar.', 'year': 2009, 'imdb_rating': 8.2, 'category': id})
        force_authenticate(request, user=user)
        # call the endpoint
        response = views.MovieList.as_view()(request)
        # check the response
        self.assertEqual(response.status_code, 201)
    
    # tear down the test data
    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

# test new category with full data
class CategoryTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # create a superuser
        User.objects.create_superuser(username='admin', password='admin')

    def test_category(self):
        # authenticate as admin
        user = User.objects.get(username='admin')
        # create a request
        request = self.factory.post('/categories/', {'name': 'Test Category'})
        force_authenticate(request, user=user)
        # call the endpoint
        response = views.CategoryList.as_view()(request)
        # check the response
        self.assertEqual(response.status_code, 201)
    
    # tear down the test data
    def tearDown(self):
        Category.objects.all().delete()
        User.objects.all().delete()

class PaymentTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # create a few categories
        Category.objects.create(name='Action')
        Category.objects.create(name='Comedy')
        # create a few movies in each category
        category = Category.objects.get(name='Action')
        Movie.objects.create(title='The Matrix', description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', year=1999, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Reloaded', description='Neo has spent two years in the past looking for the one thing that he knows will bring him back to the present.', year=2003, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Revolutions', description='The human city of Zion defends itself against the massive invasion of the machines as Neo fights to end the war at another front while also opposing the rogue Agent Smith.', year=2003, imdb_rating=8.7, category=category)
        # create a few django users
        User.objects.create_user(username='user1', password='user1')
        User.objects.create_user(username='user2', password='user2')
        User.objects.create_user(username='user3', password='user3')
        # create a few rentals for each user
        user = User.objects.get(username='user1')
        movie = Movie.objects.get(title='The Matrix')
        # create a rental for user and movie with rented_at 5 days before datetime.datetime.now()
        Rental.objects.create(customer=user, movie=movie, rented_at=datetime.datetime.now() - datetime.timedelta(days=5))

    def test_payment(self):
        # grab 'The matrix' rental id from the database
        rental = Rental.objects.get(movie__title='The Matrix')
        id = rental.id
        # authenticate user1
        user = User.objects.get(username='user1')
        # create a payment request as authenticated user with amount of 10
        request = self.factory.post('/payments/', {'rental': id, 'amount': 10})
        force_authenticate(request, user=user)
        # call the endpoint as authenticated user
        response = views.PaymentList.as_view()(request)
        # response should be 400
        self.assertEqual(response.status_code, 400)
    
    # tear down the test data
    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        Rental.objects.all().delete()


class PaymentTest2(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # create a few categories
        Category.objects.create(name='Action')
        Category.objects.create(name='Comedy')
        # create a few movies in each category
        category = Category.objects.get(name='Action')
        Movie.objects.create(title='The Matrix', description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', year=1999, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Reloaded', description='Neo has spent two years in the past looking for the one thing that he knows will bring him back to the present.', year=2003, imdb_rating=8.7, category=category)
        Movie.objects.create(title='The Matrix Revolutions', description='The human city of Zion defends itself against the massive invasion of the machines as Neo fights to end the war at another front while also opposing the rogue Agent Smith.', year=2003, imdb_rating=8.7, category=category)
        # create a few django users
        User.objects.create_user(username='user1', password='user1')
        User.objects.create_user(username='user2', password='user2')
        User.objects.create_user(username='user3', password='user3')
        # create a few rentals for each user
        user = User.objects.get(username='user1')
        movie = Movie.objects.get(title='The Matrix')
        # create a rental for user and movie with rented_at today
        Rental.objects.create(customer=user, movie=movie, rented_at=datetime.datetime.now())
      
    def test_payment(self):
        # grab 'The matrix' rental id from the database
        rental = Rental.objects.get(movie__title='The Matrix')
        id = rental.id
        # authenticate user1
        user = User.objects.get(username='user1')
        # create a payment request
        request = self.factory.post('/payments/', {'rental': id, 'amount': 1})
        force_authenticate(request, user=user)
        # call the endpoint
        response = views.PaymentList.as_view()(request)
        # response should be 201 as payment was successful
        self.assertEqual(response.status_code, 201)
    
    # tear down the test data
    def tearDown(self):
        Movie.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        Rental.objects.all().delete()