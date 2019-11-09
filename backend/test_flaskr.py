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

            category1 = Category(type='IT')
            category2 = Category(type='Sport')
            self.db.session.add_all([category1, category2])
            self.db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            categories = self.db.session.query(Category).all()
            for category in categories:
                self.db.session.delete(category)
                self.db.session.commit()

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
