from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

# database_path = os.environ['DATABASE_URL']

# database_name = "moneytrack"
# database_path = "postgres://{}/{}".format('sterl:majetich1@localhost:5432', database_name)

database_path = os.environ.get("DATABASE_URL")

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
Expenditure--represents one act of money-spending
'''
class Expenditure(db.Model):
  __tablename__ = 'Expenditure'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  amount = Column(Integer) # in cents
  expenditure_categories = db.relationship('expenditure_categories', backref="expenditure", lazy=True)


  def __init__(self, name, amount, category_id):
    self.name = name
    self.amount = amount

  def dict_form(self):
    return {
      'id': self.id,
      'name': self.name,
      'amount': self.amount,
      'category_id': self.category_id,
      }

'''
Category--represents one category of expenditure
'''
class Category(db.Model):
  __tablename__ = 'Category'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  expenditure_categories = db.relationship("expenditure_categories", backref='category', lazy=True)

  def __init__(self, name):
    self.name = name

  def dict_form(self):
    return {
      'id': self.id,
      'name': self.name
    }

class ExpenditureCategory(db.Model):
  __tablename__ = "ExpenditureCategory"
  id = Column(Integer, primary_key=True)
  expenditure_id = Column(Integer, ForeignKey('Expenditure.id'))
  category_id = Column(Integer, ForeignKey('Category.id'))
