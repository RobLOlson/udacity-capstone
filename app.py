import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Expenditure, Category
from sqlalchemy import text

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    setup_db(app)
    CORS(app)

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    @app.route("/expenditures")
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

    @app.route("/expenditures/<int:expense_id>", methods=["PATCH", "DELETE"])
    def update_expenditure(expense_id):
      # if id is zero, use last submitted
      if expense_id == 0:
        target_expense = Expenditure.query.order_by(text("id desc")).first()
      else:
        target_expense = Expenditure.query.get(expense_id)

      if request.method == "PATCH":
        target_expense.update(request.json)
        return jsonify({
          "success": True,
          "expenditure": target_expense.dict_form(),
        })

      if request.method == "DELETE":
        target_expense.delete()
        all_expenditures = Expenditure.query.all()
        return jsonify({
          "success": True,
          "expenditures": [e.dict_form() for e in all_expenditures]
          })

    @app.route("/categories")
    def get_categories():
      all_categories = Category.query.all()
      return jsonify({
        "success": True,
        "categories": [e.dict_form() for e in all_categories],
        })

    @app.route('/categories', methods=["POST"])
    def add_category():
      new_category = Category(**request.json)
      new_category.insert()
      return jsonify({
        "success": True,
        "category": new_category.dict_form(),
        })

    @app.route('/categories/<int:category_id>', methods=["PATCH", "DELETE"])
    def update_category(category_id):
      # if ID is zero, use last submitted
      if category_id == 0:
        target_category = Category.query.order_by(text("id desc")).first()
      else:
        target_category = Category.query.get(category_id)

      if request.method=="PATCH":
        target_category.update(request.json)
        return jsonify({
          "success": True,
          "expenditure": target_category.dict_form()
          })

      if request.method=="DELETE":
        target_category.delete(request.json)
        all_categories = Category.query.all()
        return jsonify({
          "success": True,
          "categories": [e.dict_form() for e in all_categories]
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
