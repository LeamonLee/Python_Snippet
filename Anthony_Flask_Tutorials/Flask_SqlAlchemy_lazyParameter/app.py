from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myDatabase.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    
    # With this lazy parameter means is how the data for the relationship is loaded.
    # Typically, when you run a query, you get everything back all at once.
    # But if you change lazy to something else, your data may load at the beginning, 
    # or may load later on when you actually start accessing datas. 
    pets = db.relationship("Pet", backref="owner", lazy="dynamic")      # "Pet" is a class in your python code, so needs to be uppercase
    # backref will create a virtual column in Pet model to reference back to Person. 

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey("person.id"))    # "person.id" is the actual table name in your database, so needs to be lowercase.