import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Expenditure, Category
import requests

APP_URL = os.environ.get("APP_URL")

ADMIN_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxCa0EyUmJRNWFlYS1lQndPWDRLNiJ9.eyJpc3MiOiJodHRwczovL3JvYmxvdWlzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWFhMGNlMTZiNjliYzBjMTJlNDBlODUiLCJhdWQiOiJtb25leWFwaSIsImlhdCI6MTU5MDAzMTI0OCwiZXhwIjoxNTkwMTE3NjQ4LCJhenAiOiI0MFBzMFE0WnBzd1ljNzF6RjlvVVUzRTVRSE01UHJwaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmV4cGVuZGl0dXJlcyIsInBhdGNoOmV4cGVuZGl0dXJlcyIsInBvc3Q6ZXhwZW5kaXR1cmVzIiwicmVhZDpleHBlbmRpdHVyZXMiXX0.T3XsY0XqOjRc8sUH7TKcMAuqJTZepxGlI7gfxQn2JXaAsS8qWGwjbju-v-0ZlmLWUeVh1ieYVPjodMjoTJ6mdtfCzUMZjR_MDnhwJ8-k4b4yPbBEt395ka94dtRpiAJy7ldrArHRimvSNh2ZmXPhVU3TI3YM0e7uqZ_f6fhX7wiZAj1ukMwZ6DVxY3Qgg8UXJt7-AKBcaFcCMD5im3GfYuO1pxtAlr3Jvj29keOI0XNqQVsHG6nolH1FDUxgx33kk02gklIHI3wy39pejCX08R-lb7nO81UlbWk21vW_J-ycpSvJHSc-RCQ7DqTI2Z8biRV9xAen87Bs6C9aLYL9CA"

ADMIN_AUTH_HEADER = {"Authorization": ADMIN_TOKEN}

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

    def test_new_expenditures(self):
        new_name = "".join(random.choices("abcdefghijklmn", k=10))
        new_amount = random.randint(1, 999)
        db_old_size = len(Expenditure.query.all())
        new_expense = {"name": new_name, "amount": new_amount}
        resp = requests.post(APP_URL+"/expenditures", json = new_expense, headers = ADMIN_AUTH_HEADER)

        data = resp.json()
        db_new_size = len(Expenditure.query.all())

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(db_old_size+1, db_new_size)
        self.assertTrue(data['success'])

    def test_delete_expenditures(self):
        db_old_size = len(Expenditure.query.all())
        valid_ids = [el.id for el in Expenditure.query.all()]
        resp = requests.delete(APP_URL+f'/expenditures/{valid_ids[-1]}', json={}, headers=ADMIN_AUTH_HEADER)
        data = resp.json()
        db_new_size = len(Expenditure.query.all())

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(db_old_size-1, db_new_size)
        self.assertTrue(data['success'])

    def test_invalid_new_expense_json(self):
        resp = requests.post(APP_URL+'/expenditures', json={}, headers=ADMIN_AUTH_HEADER)
        data = resp.json()

        self.assertEqual(data['error'], 422)
        self.assertFalse(data['success'])

    def test_invalid_expense_delete(self):
        resp = requests.delete(APP_URL+'/expenditures/10000', json={}, headers=ADMIN_AUTH_HEADER)
        data = resp.json()

        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    def test_category_list(self):
        resp = self.client().get('/categories/1/questions', json={})
        data = json.loads(resp.data)

 #        self.assertEqual(resp.status_code, 200)
 #        self.assertTrue(data['success'])
 #        self.assertTrue(data['total_questions'])

 #    def test_get_quizzes(self):
 #        resp = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": {"type": "Science", "id": 1}})
 #        data = json.loads(resp.data)

 #        self.assertEqual(resp.status_code, 200)
 #        self.assertTrue(data['success'])


    def test_invalid_url(self):
        resp = requests.get(APP_URL+'/does_not_exist', json={})
        data = resp.json()

        self.assertEqual(resp.status_code, 404)
        self.assertFalse(data['success'])



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

