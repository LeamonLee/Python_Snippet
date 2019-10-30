from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reward_name = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='rewards')

# Don't have to create every attribute one by one in class. Just specify the python class to model.
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User 

class RewardSchema(ma.ModelSchema):
    class Meta:
        model = Reward

@app.route('/')
def index():
    users = User.query.all()
    user_schema = UserSchema(many=True)             # Needs to set many=True if there are multiple users.
    output = user_schema.dump(users).data           # serialize: complex python data type --> simple python data type
    return jsonify({'user' : output})

if __name__ == '__main__':
    app.run(debug=True)
