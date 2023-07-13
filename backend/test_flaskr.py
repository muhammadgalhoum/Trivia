import os
import unittest
import json

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Executed before each test. Define test variables and initialize app."""
        
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        DB_USER = os.environ.get("DB_USER")
        DB_URL = os.environ.get("DB_URL")
        
        self.app = create_app(test_config={'DATABASE_URL': f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}"})
        self.client = self.app.test_client
        with self.app.app_context():
            db.create_all()
        
        self.new_question = {
        "question": "How many planets are there in the Universe?",
        "answer": "Nine",
        "category" : "1",
        "difficulty": 2,
        }
    
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
        
    def test_get_categories_success(self):
        response = self.client().get('/categories')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 1)

    def test_get_categories_error(self):
        # Simulate an error by deleting all categories from the database
        with self.app.app_context():
            Category.query.delete()
            db.session.commit()

        response = self.client().get('/categories')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 0)
       
        
    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_questions"])

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post("/questions/1", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    
    
    def test_get_question_search_with_results(self):
        res = self.client().post("/questions/search", json={"searchTerm": "How many planets are there in the Universe?"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 1)
        self.assertTrue(len(data["questions"]), 1)

    def test_get_question_search_without_results(self):
        res = self.client().post("/questions/search", json={"searchTerm": "Who invented Peanut Butter?"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)
    
    
    def test_delete_question(self):
        with self.app.app_context():
            res = self.client().delete("/questions/4")
            data = json.loads(res.data)

            question = Question.query.filter(Question.id == 4).one_or_none()

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)
            self.assertEqual(data["deleted"], 4)
            self.assertTrue(len(data["questions"]))
            self.assertTrue(data["total_questions"])
            self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")   
     
        
    def test_questions_by_category_success(self):
        category_id = 1

        response = self.client().get(f'/categories/{category_id}/questions')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertIn('current_category', data)

    def test_questions_by_category_error(self):
        category_id = 999

        response = self.client().get(f'/categories/{category_id}/questions')
        data = response.get_json()

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')
    
    
    def test_play_quiz_success(self):
        quiz_category = {"id": 1, "type": "Science"}
        previous_questions = [1, 2]
        response = self.client().post('/quizzes', json={"quiz_category": quiz_category, "previous_questions": previous_questions})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('question', data)
        self.assertNotIn('previous_questions', data)
        
    def test_play_quiz_failure(self):
        quiz_category = {"id": 1, "type": "Science"}
        previous_questions = [1, 2, 3, 4, 5]
        response = self.client().post('/quizzes', json={"quiz_category": quiz_category, "previous_questions": previous_questions})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['question'], None)
        self.assertNotIn('previous_questions', data)
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()