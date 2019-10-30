from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myDatabase.db"

db = SQLAlchemy(app)

# if you want to have a many-to-many relationship,
# have to define an association table to make the connection between User Table and Channel Table.
subsMapping = db.Table("subsMapping", 
                db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                db.Column("channel_id", db.Integer, db.ForeignKey("channel.id")))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    subscriptions = db.relationship("Channel", secondary=subsMapping, backref=db.backref("viewers", lazy="dynamic"))

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    