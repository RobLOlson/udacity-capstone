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
  category_id = db.Column(Integer, ForeignKey('Category.id'))
  category = db.relationship('Category', backref="expenditures", lazy=True)


  def __init__(self, name, amount, category_id=None):
    self.name = name
    self.amount = amount
    self.category_id=category_id

  def __repr__(self):
    return f"<Expenditure({self.name})[#{self.id}]>"

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self, target_dict):
    for key in target_dict.keys():
      if key in ["name", "amount", "category_id"]:
        setattr(self, key, target_dict[key])
    db.session.commit()

  def undo(self):
    db.session.rollback()

  def dict_form(self):
    return {
      'id': self.id,
      'name': self.name,
      'amount': self.amount,
      'category_id': self.category_id,
      }

# </END OF class Expenditure(name, ...)>


'''
Category--represents one category of expenditure
'''
class Category(db.Model):
  __tablename__ = 'Category'

  id = Column(Integer, primary_key=True)
  name = Column(String)

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return f"<Category({self.name})[#{self.name}]>"

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def undo(self):
    db.session.rollback()

  def dict_form(self):
    return {
      'id': self.id,
      'name': self.name
    }
