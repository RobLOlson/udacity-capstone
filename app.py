import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import models

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  models.setup_db(app)

  return app

app = create_app()

@app.route("/")
def index():
  return "HELLO"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
