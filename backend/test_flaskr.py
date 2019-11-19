
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):

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

            sport_category = self.db.session.query(Category).filter(Category.type == 'Sport').first()
            history_category = self.db.session.query(Category).filter(Category.type == 'History').first()

            q1 = Question(
                question="According to one study, how many minutes are actually played during the average "
                         "American football game?",
                answer="25",
                category=str(sport_category.id),
                difficulty=0
            )

            q2 = Question(
                question="After the 'Mona Lisa' was stolen from the Louvre in 1911, which famous artist was "
                         "considered a suspect?",
                answer="Pablo Picasso",
                category=str(history_category.id),
                difficulty=1
            )

            q3 = Question(
                question="Who is the Best Soccer Player ever",
                answer="Ronaldo",
                category=str(sport_category.id),
                difficulty=2
            )
            self.db.session.add_all([q1, q2, q3])
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
        self.assertEqual(data['categories'][0]['type'], 'Sport')
        self.assertEqual(data['categories'][1]['type'], 'History')

    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 3)
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 3)
        self.assertTrue(data['current_category'] in data['categories'])

    def test_pagination(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'], [])
        self.assertEqual(data['total_questions'], 3)
        self.assertTrue(data['current_category'] in data['categories'])

    def test_delete_question(self):
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            question = self.db.session.query(Question).first()

        res = self.client().delete('/questions/{}'.format(question.id))
        self.assertEqual(res.status_code, 200)

    def test_negative_delete_question(self):
        res = self.client().delete('/questions/2345678945655')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not Found')
        self.assertEqual(data['success'], False)

    def test_create_question(self):
        res = self.client().post('/questions', json={
            'question': 'What is my name',
            'answer': 'Gil',
            'category': '23',
            'difficulty': 3
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_negative_create_question(self):
        res = self.client().post('/questions', json={
            'question': 'What is my name',
            'answer': 'Gil',
            'category': 'ab',
            'difficulty': 3
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")

    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'American'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['questions'][0]['question'], "According to one study, how many minutes are actually "
                                                           "played during the average American football game?")

    def test_questions_by_categories(self):
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            category = self.db.session.query(Category).filter(Category.type == 'History').all()

        res = self.client().get('/categories/{}/questions'.format(category[0].id))
        self.assertEqual(res.status_code, 200)

    def test_negative_questions_by_categories(self):
        res = self.client().get('/categories/2000005697/questions')
        self.assertEqual(res.status_code, 404)

    def test_quizz(self):
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            question = self.db.session.query(Question).filter(Question.answer == 'Ronaldo').first()

        res = self.client().post('/quizzes', json={"previous_questions": [question.id]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(data['question']["question"], 'Who is the Best Soccer Player ever')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
