import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
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
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    def pagination(_request):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return start, end, page

    @app.route('/categories')
    def get_categories():
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
        try:
            question = db.session.query(Question).get(question_id)
            question.delete()
            return '', 204
        except Exception as err:
            logging.error(err)
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            if request.headers['Content-Type'] == 'application/json':
                request_body = request.json
                question = Question(
                    question=request_body.get('question'),
                    answer=request_body.get('answer'),
                    category=request_body.get('category'),
                    difficulty=int(request_body.get('difficulty'))
                )
                db.session.add(question)
                db.session.commit()
                return jsonify({'status': 'successful'}), 201
        except Exception as err:
            print(err)
            abort(422)

    # TODO: Create a POST endpoint to get questions based on a search term.
    #  It should return any questions for whom the search term is a substring of the question.
    '''
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions/<string:search_phrase>')
    def search_questions(search_phrase):
        try:
            questions = db.session.query(Question).filter_by(
                Question.question.ilike('%{}%'.format(search_phrase))).all()
            formatted_questions = [question.format() for question in questions]
            start, end, page = pagination(request)
            return jsonify({
                'success': True,
                'questions': formatted_questions[start:end],
                'total_questions': len(formatted_questions),
                'page': page
            }), 200
        except Exception as err:
            print(err)
            abort(422)

    # TODO: Create a GET endpoint to get questions based on category.

    '''
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_based_on_category(category_id):
        category = db.session.query(Category).get(category_id)
        if category is None:
            abort(404)
        try:
            questions = db.session.query(Question).filter(Question.category == str(category.id)).all()
            formatted_questions = [question.format() for question in questions]
            start, end, page = pagination(request)
            return jsonify({
                'success': True,
                'questions': formatted_questions[start:end],
                'total_questions': len(formatted_questions),
                'current_category': category
            }), 200
        except Exception as err:
            logging.error(err)
            abort(422)

    # TODO: Create a POST endpoint to get questions to play the quiz.
    #  This endpoint should take category and previous question parameters
    #  and return a random questions within the given category, if provided,
    #  and that is not one of the previous questions.

    '''
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

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

    return app
