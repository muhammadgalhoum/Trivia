# The Trivia Project with it's API Documentation

Trivia is a dynamic web app that offers a wide range of features for trivia enthusiasts. Users can explore and paginate through an extensive question database, filter questions by category, and search for specific terms. They can also add new questions to expand the collection. Engaging quizzes allow users to test their knowledge, while the delete feature provides control over questions. Enjoy interactive trivia experiences and endless learning opportunities with Trivia.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have Python3 and pip installed on their local machines.

## Backend

Set up a virtual environment by running this command `python -m venv env`, then to activate the virtual environment by running this command `.\env\Scripts\activate`.  

From the main directory run `pip install -r requirements.txt`. All required packages are included in the requirements.txt file.

To run the application run the following commands:

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
set FLASK_DEBUG=true
flask run
```

These commands put the application in development and direct our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.

The application is run on `http://127.0.0.1:5000/` by default.

## Frontend

### Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected.

### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: `npm i`is shorthand for `npm install``

### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

### Tests

In order to run tests, open new terminal and make sure you are in the main directory in front of `test
_flaskr.py` file  run the following command:

```bash
python test_flaskr.py
```

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started with API Documentation

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```bash
{
  "success": False, 
  "error": 400,
  "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable

### Endpoints

#### GET /categories

- General:
  - Returns a list of category objects and success value.
  
- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": [
      "Science",
      "Art",
      "Geography",
      "History",
      "Entertainment",
      "Sports"
  ],
  "success": true
}
```

#### GET /categories/{category_id}/questions

- General:
  - Returns the current category, a list of questions based on the current category id, success value, and total questions.
  
- Sample: `curl http://127.0.0.1:5000/categories/5/questions`

```json
{
  "current_category": "5",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

#### GET /questions

- General:
  - Returns a list of category objects and also a list of question objects, success value, and total number of questions.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

- Sample: `curl http://127.0.0.1:5000/questions`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```

#### POST /questions{question}

- General:
  - Get questions based on a search term. It returns any questions for whom the search term is a substring of the question.

  - Returns a list of matching questions, success value, and total questions.

- `curl -X POST -H "Content-Type: application/json" -d "{\"searchTerm\": \"penicillin?\"}" /questions/search`

```json
{
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### POST /questions

- General:
  - Creates a new question using the submitted question, answer, category and difficulty.

  - Returns the id of the created question, success value, total questions.

- `curl -X POST -H "Content-Type: application/json" -d "{\"question\": \"What is the hardest natural substance on Earth?\", \"answer\": \"Diamond\", \"category\": \"1\", \"difficulty\": \"3\"}" http://127.0.0.1:5000/questions`

```json
{
  "created": 27,
  "success": true,
  "total_questions": 22
}
```

#### DELETE /questions/{question_id}

- General:
  - Deletes the question of the given ID if it exists.

  - Returns the id of the deleted question, success value, total questions, and questions list based on the current page number to update the frontend.

- `curl -X DELETE http://127.0.0.1:5000/questions/27`

```json
{
  "deleted": 27,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```

#### POST /quizzes

- General:
  - Returns a random question which not in the previous questions list but in the chosen category.

- `curl -X POST -H "Content-Type: application/json" -d "{\"category\": \"science\", \"previous_questions\": [1, 2, 3]}" http://localhost:5000/quizzes`

```json
{
  "question": {
    "answer": "Muhammad Ali",
    "category": "4",
    "difficulty": 1,
    "id": 9,
    "question": "What boxer's original name is Cassius Clay?"
  },
  "success": true
}
```

## Deployment N/A

## Authors

Yours truly, Software Developer Muhammad Galhoum

## Acknowledgements N/A
