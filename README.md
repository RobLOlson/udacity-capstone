# Full Stack Capstone Project: Money Track

## Description of Money Track

The goal of this project is to create a simple API for tracking categorized expenditures.  This project should demonstrate the principles and follow the best practices of API design, Role Based Access Control, automated testing, third-party authentication and deployment.

### Code Style

The code in this project should follow PEP8 guidelines.

## Getting Started

### Prerequisites

Depedencies can be installed using pip:
    pip install -r requirements.txt

Auth0 and Heroku accounts are required to run and deploy the server.  Configuration for using these services (URLs, secrets, etc.) should be stored in the file ".autoenv".  For deployment, Heroku settings should be configured with production ready config values.

### Local Development

The API server can be run locally on port 5000 by pointing FLASK_APP environment variable at "app.py".  Then invoke flask with "flask run".

Alternatively, you can run the server by feeding the app.py to the python interpreter:

    python __init__.py

### Tests

Endpoint tests are written in Postman and stored in file "Capstone.postman_collection.json".  Run the backend endpoint tests from within Postman.

Additionally, pure python unit tests are included and can be run locally by invoking pytest (make sure local server is running).  Tests can also be run on heroku directly with the following command:

    heroku run pytest

## API Reference

### Base URL

Server is hosted locally on "localhost:5000".  A public facing server is hosted on heroku at http://moneytracklol.herokuapp.com

### Errors

Response codes

  * 200 (Success)
  * 401 (Unauthorized)
  * 404 (Expense not found)
  * 405 (Method not allowed)
  * 422 (Malformed JSON)

### Role Based Access

  GET requests are unrestricted.

  The 'user' role has permission to POST and PATCH expenditures and categories.  The 'admin' has all 'user' permissions, plus DELETE permissions.

  Users should authenticate with Auth0 to receive a Json-Web Token.  Use that token as a bearer token in the request's Authorization Header.

### Endpoints

#### Expenditures

    /expenditures (GET moneytracklol.herokuapp.com/expenditures)

  Allowed methods: GET, POST.

  GET returns all expenditures as JSON.
  POST submits a new expenditure from JSON body (must include "name" and "amount").

    /expenditures/<int:expense_id> (PATCH moneytracklol.herokuapp.com/questions/1)

  Allowed methods: GET, PATCH, DELETE

  Gets/posts/deletes a specific expenditure.  Only the 'admin' role can use DELETE.  If you supply a zero for expense_id, server will act accordingly on the most recent expenditure.


#### Categories

    /categories (GET moneytracklol.herokuapp.com/categories)

  Allowed methods: GET, POST.

  GET returns all categories.
  POST submits a new category from JSON body (must include "name").

    /categories/<int:category_id> (PATCH moneytracklol.herokuapp.com/categories/1)

  Allowed methods: GET, PATCH, DELETE

  Gets/posts/deletes a specified category.  Only the 'admin' role can use DELETE.  If you supply a zero for category_id, server will act accordingly on the most recent category.

## Authors

Robert Olson

## Acknowledgements

Thanks to Udacity for making this awesome full stack web development class!
