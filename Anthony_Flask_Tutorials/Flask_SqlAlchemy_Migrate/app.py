from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myDatabase.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# These two lines seem can be removed.
# manager = Manager(app)
# manager.add_command("db", MigrateCommand)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    pets = db.relationship("Pet", backref="owner")      # "Pet" is a class in your python code, so needs to be uppercase
    # backref will create a virtual column in Pet model to reference back to Person. 


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey("person.id"))    # "person.id" is the actual table name in your database, so needs to be lowercase.



if __name__ == "__main__":
    manager.run()
