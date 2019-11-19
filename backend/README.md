# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## REST Resource

**Getting Started**
- Base URL: This app is hosted locally and the default url is http://127.0.0.1:5000/
- Authentication: This version of the application does not require authentication or API keys.

**Error Handling**
```
{
  "error": 404,
  "message": "Resource not Found",
  "success": false
}
```
The API will return one of 4 error types when request fails.
- 400: Bad Request
- 404: Resource Not Found
- 422: Unprocessable Entity
- 500: Internal Server Error

**Endpoints**


GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with keys (categories and success) that categories contain a dictionary of with keys id and type, success is a boolean value. 
- Sample: curl http://127.0.0.1:5000/categories
```
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true
}
```

GET '/questions'
- Fetches a dictionary of all questions, current category and total questions. Pagination of 10 questions per page is in effect
- Request Arguments: page, default is 1 
- Returns: An object with keys (questions, categories, current_category, success, total_questions)
- Sample: curl http://127.0.0.1:5000/questions
```
{
  "categories": [
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "current_category": {
    "id": 1,
    "type": "Science"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

POST '/questions'
- Creates a question
- Request Arguments: None
- Returns: 201 response
- Sample: curl -data '{"question":"What is my name", "answer": "John", "category": "2", "difficulty": "3"}' -H "Content-Type: application/json" -X ttp://http://127.0.0.1:5000/questions
```
{
  "success": true
}
```

POST '/questions'
- Get questions based on a search term, search is case insensitive
- Request Arguments: None
- Sample: curl -d '{"searchTerm":"vinci"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/questions
```
{
  "currentCategory": {
    "id": 1,
    "type": "Art"
  },
  "questions": [
    {
      "answer": "Vinci",
      "category": "1",
      "difficulty": 3,
      "id": 1,
      "question": "In which town was Leonardo da Vinci born?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

GET '/categories/{categoryId}/questions'
- Fetches questions based on category
- Request Arguments: None
- Returns: An object with keys (questions, current_category, success, total_questions)
- Sample: http://127.0.0.1:5000/categories/4/questions
```
{
  "current_category": {
    "id": 4,
    "type": "History"
  },
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

POST '/quizzes'
- Fetches questions to play the quiz
- Request Body: json with two keys(quiz_category, previous_questions), category id and a list of previous question ids
- Return: A random question within the given category, if provided, and that is not one of the previous questions
- Sample: http://127.0.0.1:5000/quizzes
```
{
  "question": {
    "answer": "Vulture",
    "category": "5",
    "difficulty": 4,
    "id": 6,
    "question": "In Disney’s The Jungle Book what kind of animal is Ringo? Monkey, snake, vulture, elephant"
  }
}
```

DELETE '/questions/{questionId}'
- Deletes a question
- Sample: http://127.0.0.1:5000/questions/5
```
{
  "success": true
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
python test_flaskr.py
```