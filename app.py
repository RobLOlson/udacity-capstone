import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Expenditure, Category, ExpenditureCategory


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    setup_db(app)
    CORS(app)

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    @app.route("/")
    def index():
      all_expenses = Expenditure.query.all()
      return jsonify({
        "success": True,
        "expenditures": [e.dict_form() for e in all_expenses],
        })

    @app.route("/expenditures", methods=["POST"])
    def add_expenditure():
      new_expense = Expenditure(**request.json)
      new_expense.insert()
      return jsonify({
        "success": True,
        "expenditure": new_expense.dict_form(),
        })

    @app.errorhandler(400)
    def handle_error_400(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": error.description,
            }), 400

    @app.errorhandler(401)
    def handle_error_401(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": error.description,
            }), 401


    @app.errorhandler(403)
    def handle_error_403(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": error.description,
            }), 403

    @app.errorhandler(404)
    def handle_error_404(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": error.description,
            }), 404

    @app.errorhandler(422)
    def handle_error_402(error):
        return jsonify({
            "success": False,
            "error": 402,
            "message": error.description,
            })
    return app

app = create_app()


if __name__ == '__main__':
    app.run()
