import random, os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is not None:
      # Use the test database URL from the test configuration
        database_url = test_config['DATABASE_URL']
    else:
        # Use the development database URL as a default
        
        DB_PASSWORD=os.environ.get("DB_PASSWORD")
        DB_USER=os.environ.get("DB_USER")
        DB_URL=os.environ.get("DB_URL")
        database_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}'
            
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    with app.app_context():
        db.init_app(app)
        db.create_all()
    
    CORS(app, origins='*')
    
    
    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response


    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions
    
    
    @app.route('/categories', methods=["GET"])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = [category.type for category in categories]

        return jsonify({
            "success": True,
            "categories": formatted_categories
        })


    @app.route("/questions", methods=["GET"])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.order_by(Category.id).all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": categories_dict,
            }
        )
    
        
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            
            question.delete()
            
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(422)
    

    @app.route("/questions", methods=["POST"])
    def craete_questions():
        body = request.get_json()

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_difficulty = body.get('difficulty')
        new_category = body.get('category')

        try:
            question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            question.insert()

            return jsonify({
                "success": True,
                "created": question.id,
                "total_questions": len(Question.query.all())
            })
        except:
            abort(422)
    
    
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        search_term = request.get_json().get("searchTerm", None)

        if search_term:
            selection = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(selection)
                }
            )
        else:
            abort(404)

    
    @app.route("/categories/<string:category_id>/questions", methods=["GET"])
    def questions_by_category(category_id):
        try:
            selection = Question.query.filter(Question.category == category_id)
            current_questions = paginate_questions(request, selection)
            
            if not current_questions:
                abort(404)  # Raise an exception if no questions found for the category

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(selection.all()),
                    "current_category": category_id,
                }
            )

        except:
            abort(422)
    
    
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()

        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')

        category_id = None
        if quiz_category:
            category_id = quiz_category['id'] 
        
        if category_id:
            category_id = str(int(quiz_category['id']) + 1) 
            questions = Question.query.filter_by(category=category_id).all()
        else:
            questions = Question.query.all()

        available_questions = [question for question in questions if question.id not in previous_questions]

        if available_questions:
            selected_question = random.choice(available_questions)
            formatted_question = selected_question.format()
            return jsonify({
                'success': True,
                'question': formatted_question
            })
        else:
            return jsonify({
                'success': True,
                'question': None
            })
    
    
   # Handling Errors
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
        }), 404
    
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
        }), 405
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app