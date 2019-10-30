from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myDatabase.db"

db = SQLAlchemy(app)


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    child = db.relationship("Child", backref="parent", uselist=Flase)   # To make a one-to-one relationship, set uselist=False

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    parent_id = db.Column(db.Integer, db.ForeignKey("parent.id"), unique=True)    # "person.id" is the actual table name in your database, so needs to be lowercase.