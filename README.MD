# Assignment
## Online Movies Rent Store

Create a proof of concept app of an “Online Movies Store” from where users can perform all the
base actions in order to search and rent/book and pay an online movie ”Title”. When the user
purchase a “Title” he/she can play the movie as many times as he/she wants and the charge is
based on a per day fee.

Use cases:
* User can get a list of all available movies.
* User can get a list of available movies based on criterias example (category).
* User can navigate and get the details/info of a specific movie.
* User can “rent” a movie (make available for play).
* User can “return” a movie.
* User get the charge (“amount of money”) based on days.
* User is charged 1 EU per day for the first three days and 0,5 EU per day for the days after the
first three.

# Introduction
This is a proof of concept app of an “Online Movies Store”. The app is based on a RESTful API. It has been developed using the following technologies:
* Docker
* Django Rest Framework
* PostgreSQL

Use cases have been divided into the following categories:
* Unauthenticated users (They can get a list of all available movies and categories and navigate and get the details/info of a specific movie).
* Authenticated users (They can rent a movie (create a new rental), pay for it (create a new payment) and return it (delete rental).
* Superusers (They can create a new movie, update a movie, delete a movie, create a new category, update a category, delete a category etc.)

# Installation
The app is docker based and can be built using the docker-compose file.
```
docker-compose build
```
# Usage
The app is running on port 8000. The app is accessible from the browser or using the command line.
In order to run the app you just need to run the command:
```
docker-compose up
```

# Superuser creation
The superuser can be created using the following command:

```
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```
# Testing

There are a few tests that can be run using the command line:
```
docker-compose run --rm app sh -c "python manage.py test"
```

# Endpoints
## Authentication

* POST /token/
    * Returns an ACCESS_TOKEN and a REFRESH_TOKEN for the given username and password.
    ```
    curl -H 'Content-Type: application/json' -X POST http://localhost:8000/token/ -d '{"username":"test", "password":"test"}'
    ```
* POST /token/refresh/
    * When the ACCESS_TOKEN expires, the user can use this endpoint to obtain another one.
    ```
    curl -H 'Content-Type: application/json' -X POST http://localhost:8000/token/refresh/ -d '{"refresh":"REFRESH_TOKEN"}'
    ```
* PROVING AUTHENTICATION
    * The user can use the ACCESS_TOKEN to prove that he/she is authenticated by adding the header 'Authorization: Bearer ACCESS_TOKEN' to the request.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN'
    ```
## Unauthenticated

* GET /movies/:
    * Returns a list of all available movies.
    * Returns a list of available movies based on criterias (title, description, category, year)
    ``` 
    curl -X GET http://localhost:8000/movies/?title=The+Matrix
    ```
* GET /movies/:id/
    * Returns the details of a specific movie.
    ```
    curl -X GET http://localhost:8000/movies/1/
    ```
* GET /categories/:
    * Returns a list of all available categories.
    ```
    curl -X GET http://localhost:8000/categories/
    ```
* GET /categories/:id/
    * Returns the details of a specific category.
    ```
    curl -X GET http://localhost:8000/categories/1/
    ```
* GET /categories/:id/movies/
    * Returns a list of all available movies based on a specific category.
    ```
    curl -X GET http://localhost:8000/categories/1/movies/
    ```
* POST /users/
    * Creates a new user with the given data (username, password).
    ```
    curl -H 'Content-Type: application/json' -X POST http://localhost:8000/users/ -d '{"username":"test", "password":"test"}'
    ```
## Authenticated
    
* POST /movies/:id/rentals/
    * Creates a new rental for the given movie if there is no active rental for the movie.
    ```
    curl -H 'Content-Type: application/json' -H 'Authorization: Bearer ACCESS_TOKEN' -X POST http://localhost:8000/movies/1/rentals/ -d '{}'
    ```
* GET /movies/:id/rentals/
    * Returns the details of the active rental for the given movie.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X GET http://localhost:8000/movies/1/rentals/
    ```
* DELETE /movies/:id/rentals/
    * Deletes the active rental for the given movie.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X DELETE http://localhost:8000/movies/1/rentals/
    ```
* POST /movies/:id/payments/
    * Creates a new payment for the given movie, price has to be provided and equal to the rental price.
    ```
    curl -H 'Content-Type: application/json' -H 'Authorization: Bearer ACCESS_TOKEN' -X POST http://localhost:8000/movies/1/payments/ -d '{"amount":1}'
    ```
* GET /movies/:id/payments/
    * Returns the list of all payments made by the authenticated user for the given movie.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X GET http://localhost:8000/movies/1/payments/
    ```
* GET /rentals/
    * Returns the list of all active rentals for the authenticated user.
    * Can be filtered by movie title.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X GET http://localhost:8000/rentals/?title=The+Matrix
    ```
* GET /rentals/:id/
    * Returns the details of the active rental for the given id.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X GET http://localhost:8000/rentals/1/
    ```
* DELETE /rentals/:id/
    * Deletes the active rental for the given id.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X DELETE http://localhost:8000/rentals/1/
    ```
* GET /payments/
    * Returns the list of all payments made by the authenticated user.
    * Can be filtered by movie title.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X GET http://localhost:8000/payments/
    ```
* GET /users/
    * Returns the details of the authenticated user.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X GET http://localhost:8000/users/
    ```
* PUT /users/:id/
    * Updates the details of the authenticated user.
    ```
    curl -H 'Content-Type: application/json' -H 'Authorization: Bearer ACCESS_TOKEN' -X PUT http://localhost:8000/users/1/ -d '{"username":"test", "password":"test"}'
    ```

## SUPER USER

* POST /categories/
    * Creates a new category with the given data (name).
    ```
    curl -H 'Content-Type: application/json' -H 'Authorization: Bearer ACCESS_TOKEN' -X POST http://localhost:8000/categories/ -d '{"name":"test"}'
    ```
* PUT /categories/:id/
    * Updates the details of the category with the given id.
    ```
    curl -H 'Content-Type: application/json' -H 'Authorization: Bearer ACCESS_TOKEN' -X PUT http://localhost:8000/categories/1/ -d '{"name":"test"}'
    ```
* DELETE /categories/:id/
    * Deletes the category with the given id.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X DELETE http://localhost:8000/categories/1/
    ```
* POST /movies/
    * Creates a new movie with the given data (title, description, category, year).
    ```
    curl -H 'Content-Type: application/json' -H 'Authorization: Bearer ACCESS_TOKEN' -X POST http://localhost:8000/movies/ -d '{"title":"test", "description":"test", "category":[1,2], "year":2000}'
    ```
* PUT /movies/:id/
    * Updates the details of the movie with the given id.
    ```
    curl -H 'Content-Type: application/json' -H 'Authorization: Bearer ACCESS_TOKEN' -X PUT http://localhost:8000/movies/1/ -d '{"title":"test", "description":"test", "category":[1,2], "year":2000}'
    ```
* DELETE /movies/:id/
    * Deletes the movie with the given id.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X DELETE http://localhost:8000/movies/1/
    ```
* GET /users/
    * Returns the list of all users.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X GET http://localhost:8000/users/
    ```
* GET /users/:id/
    * Returns the details of the user with the given id.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X GET http://localhost:8000/users/1/
    ```
* PUT /users/:id/
    * Updates the details of the user with the given id.
    ```
    curl -H 'Content-Type: application/json' -H 'Authorization: Bearer ACCESS_TOKEN' -X PUT http://localhost:8000/users/1/ -d '{"username":"test", "password":"test"}'
    ```
* DELETE /users/:id/
    * Deletes the user with the given id.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X DELETE http://localhost:8000/users/1/
    ```
* GET /rentals/
    * Returns the list of all rentals.
    * Can be filtered by username or movie title.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X GET http://localhost:8000/rentals/?user=test&movie=test
    ```
* GET /payments/
    * Returns the list of all payments.
    * Can be filtered by username or movie title.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X GET http://localhost:8000/payments/
    ```

* DELETE /rentals/:id/
    * Deletes the rental with the given id.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X DELETE http://localhost:8000/rentals/1/
    ```
* DELETE /payments/:id/
    * Deletes the payment with the given id.
    ```
    curl -H 'Authorization: Bearer ACCESS_TOKEN' -X DELETE http://localhost:8000/payments/1/
    ```