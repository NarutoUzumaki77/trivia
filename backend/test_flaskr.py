import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format('gilbertnwankwo', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            category1 = Category(type='Sport')
            category2 = Category(type='History')
            self.db.session.add_all([category1, category2])
            self.db.session.commit()

            q1 = Question(
                question="According to one study, how many minutes are actually played during the average "
                         "American football game?",
                answer="25",
                category="Sport",
                difficulty=0
            )

            q2 = Question(
                question="After the 'Mona Lisa' was stolen from the Louvre in 1911, which famous artist was "
                         "considered a suspect?",
                answer="Pablo Picasso",
                category="History",
                difficulty=1
            )
            self.db.session.add_all([q1, q2])
            self.db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            categories = self.db.session.query(Category).all()
            for category in categories:
                self.db.session.delete(category)

            questions = self.db.session.query(Question).all()
            for question in questions:
                self.db.session.delete(question)
            self.db.session.commit()

    def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_retrieve_empty_Categories(self):
        pass

    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 2)
        self.assertEqual(data['page'], 1)

    def test_retrieve_empty_questions(self):
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            questions = self.db.session.query(Question).all()
            for question in questions:
                self.db.session.delete(question)
            self.db.session.commit()

        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(data['page'], 1)

    def test_pagination(self):
        res = self.client().get('/questions?page=3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 2)
        self.assertEqual(data['page'], 3)

    def test_delete_question(self):
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            question = self.db.session.query(Question).first()

        res = self.client().delete('/question/{}'.format(question.id))
        self.assertEqual(res.status_code, 204)

    def test_questions_by_categories(self):
        res = self.client().get('/categories/3/questions')
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
