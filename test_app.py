import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Expenditure, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get("DATABASE_URL")
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass


    def test_get_expenditures(self):
        resp = self.client().get('/', json={})
        data = json.loads(resp.data)

        # self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['success'])
        # self.assertTrue(data['total_questions'])

 #    def test_search_questions(self):
 #        resp = self.client().post('/questions', json={"searchTerm": "who"})
 #        data = json.loads(resp.data)

 #        self.assertEqual(resp.status_code, 200)
 #        self.assertTrue(data['success'])
 #        self.assertTrue(data['total_questions'])

 #    def test_new_questions(self):
 #        db_old_size = len(Question.query.all())
 #        resp = self.client().post('/questions', json={"question": "How?",
 # "answer": "do ya do?",
 # "category": 1,
 # "difficulty": 1})
 #        data = json.loads(resp.data)
 #        db_new_size = len(Question.query.all())

 #        self.assertEqual(resp.status_code, 200)
 #        self.assertEqual(db_old_size+1, db_new_size)
 #        self.assertTrue(data['success'])
 #        self.assertTrue(data['total_questions'])

 #    def test_category_list(self):
 #        resp = self.client().get('/categories/1/questions', json={})
 #        data = json.loads(resp.data)

 #        self.assertEqual(resp.status_code, 200)
 #        self.assertTrue(data['success'])
 #        self.assertTrue(data['total_questions'])

 #    def test_get_quizzes(self):
 #        resp = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": {"type": "Science", "id": 1}})
 #        data = json.loads(resp.data)

 #        self.assertEqual(resp.status_code, 200)
 #        self.assertTrue(data['success'])

 #    def test_delete_questions(self):
 #        db_old_size = len(Question.query.all())
 #        valid_ids = [el.id for el in Question.query.all()]
 #        resp = self.client().delete(f'/questions/{valid_ids[-1]}', json={})
 #        data = json.loads(resp.data)
 #        db_new_size = len(Question.query.all())

 #        self.assertEqual(resp.status_code, 200)
 #        self.assertEqual(db_old_size-1, db_new_size)
 #        self.assertTrue(data['success'])
 #        self.assertTrue(data['total_questions'])

 #    def test_extreme_page_number(self):
 #        resp = self.client().get('/questions?page=1000', json={})
 #        data = json.loads(resp.data)

 #        self.assertEqual(resp.status_code, 404)
 #        self.assertFalse(data['success'])

 #    def test_get_questions(self):
 #        resp = self.client().get('/questions', json={})
 #        data = json.loads(resp.data)

 #        self.assertEqual(resp.status_code, 200)
 #        self.assertTrue(data['success'])
 #        self.assertTrue(data['total_questions'])

 #    def test_invalid_url(self):
 #        resp = self.client().get('/does_not_exist', json={})
 #        data = json.loads(resp.data)

 #        self.assertEqual(resp.status_code, 404)
 #        self.assertFalse(data['success'])

 #    def test_invalid_question_post_json(self):
 #        resp = self.client().post('/questions', json={})
 #        data = json.loads(resp.data)

 #        self.assertEqual(resp.status_code, 400)
 #        self.assertFalse(data['success'])

 #    def test_invalid_delete(self):
 #        resp = self.client().delete('/questions/1000', json={})
 #        data = json.loads(resp.data)

 #        self.assertEqual(resp.status_code, 404)
 #        self.assertFalse(data['success'])

 #    def test_invalid_question_post_url(self):
 #        resp = self.client().post('/questions/1', json={"question": "How?",
 # "answer": "do ya do?",
 # "category": 1,
 # "difficulty": 1})
 #        data = json.loads(resp.data)

 #        self.assertEqual(resp.status_code, 405)
 #        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

