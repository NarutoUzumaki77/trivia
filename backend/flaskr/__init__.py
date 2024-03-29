import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from random import randrange
import logging

from models import *

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        """
        get all categories from db
        :return:
        """
        try:
            categories = db.session.query(Category).all()
            formatted_category = [category.format() for category in categories]
            return jsonify({
                'success': True,
                'categories': formatted_category
            }), 200
        except Exception as err:
            logging.error(err)
            abort(422)

    @app.route('/questions')
    def get_questions():
        """
        get all questions from db
        :return:
        """
        try:
            questions = db.session.query(Question).all()
            formatted_questions = [question.format() for question in questions]
            categories = db.session.query(Category).all()
            formatted_categories = [category.format() for category in categories]
            start, end, page = pagination(request)
            return jsonify({
                'success': True,
                'questions': formatted_questions[start:end],
                'total_questions': len(formatted_questions),
                'categories': formatted_categories,
                'current_category': categories[0].format()
            }), 200
        except Exception as err:
            logging.error(err)
            abort(422)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        deletes the question with the given question id from db
        :return:
        """
        try:
            question = db.session.query(Question).get(question_id)
            question.delete()
            return jsonify({
                'success': True,
            }), 200
        except Exception as err:
            logging.error(err)
            abort(404)

    @app.route('/questions', methods=['POST'])
    def create_question():
        """
        Add a new question to db
        :return:
        """
        try:
            request_body = request.json
            if 'searchTerm' in request_body:
                formatted_questions, category = search_questions(request_body)
                return jsonify({
                    'success': True,
                    'questions': formatted_questions,
                    'total_questions': len(formatted_questions),
                    'currentCategory': category
                }), 200
            else:  # Create question
                category_id = request_body.get('category')
                try:
                    category = int(category_id)
                except:
                    return abort(422)
                question = Question(
                    question=request_body.get('question'),
                    answer=request_body.get('answer'),
                    category=category_id,
                    difficulty=int(request_body.get('difficulty'))
                )
                db.session.add(question)
                db.session.commit()
                return jsonify({'success': True}), 201
        except Exception as err:
            print(err)
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_based_on_category(category_id):
        """
        get all the questions in given category
        :return:
        """
        category = db.session.query(Category).get(category_id)
        if category is None:
            abort(404)
        try:
            questions = db.session.query(Question).filter(
                Question.category == str(category.id)).all()
            formatted_questions = [question.format() for question in questions]
            start, end, page = pagination(request)
            return jsonify({
                'success': True,
                'questions': formatted_questions[start:end],
                'total_questions': len(formatted_questions),
                'current_category': category.format()
            }), 200
        except Exception as err:
            logging.error(err)
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        """
        Fetches a random current question, while ensuring the previous
        questions from the request body is not passed back in the response as
        current question
        :return:
        """
        try:
            data = request.json
            current_question = None
            previous_questions = data.get('previous_questions', [])
            quiz_category_id = data.get('quiz_category', 0)
            if quiz_category_id is 0:
                questions = db.session.query(Question).all()
            else:
                category = db.session.query(Category).get(quiz_category_id)
                questions = db.session.query(Question).filter(
                    Question.category == str(category.id)).all()
            formatted_questions = [question.format() for question in questions]
            if len(previous_questions) + 1 <= len(formatted_questions):
                current_question = get_current_question(formatted_questions,
                                                        previous_questions)

            return jsonify({
                'question': current_question
            }), 200
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not Found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    def pagination(_request):
        """
        breaks up the questions into pages with 10 per page
        :return:
        """
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return start, end, page

    def get_current_question(formatted_questions, previous_questions):
        """
        check previous question and then return a current question that
        is not in the list of previous questions
        :return:
        """
        index = randrange(len(formatted_questions))
        current_question = formatted_questions[index]
        while current_question['id'] in previous_questions:
            index = randrange(len(formatted_questions))
            current_question = formatted_questions[index]
        return current_question

    def search_questions(request_body):
        """
        search question by key word
        :return:
        """
        search_term = request_body.get('searchTerm', None)
        if search_term is None:
            abort(422)
        else:
            try:
                questions = db.session.query(Question).filter(
                    Question.question.ilike('%{}%'.format(search_term))).all()
                formatted_questions = \
                    [question.format() for question in questions]
                start, end, page = pagination(request)
                category = db.session.query(Category).first()
                return formatted_questions[start:end], category.format()
            except Exception as err:
                print(err)
                abort(422)

    return app
