from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# database_path = os.environ['DATABASE_URL']

database_name = "moneytrack"
database_path = "postgres://{}/{}".format('sterl:majetich1@localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release year
'''
class Expenditure(db.Model):
  __tablename__ = 'expenditures'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  amount = Column(String)
  category = Column(String)

  def __init__(self, name, amount):
    self.name = name
    self.amount = amount
    self.category = category

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'amount': self.amount,
      'category': self.category,
      }

class Category(db.Model):
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  name = Column(String)

  def __init__(self, name):
    self.name = name

  def dict_form(self):
    return {
      'id': self.id,
      'name': self.name
    }
