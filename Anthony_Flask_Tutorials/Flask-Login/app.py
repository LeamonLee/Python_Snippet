# from urlparse import urlparse, urljoin
from urllib.parse import urlparse, urljoin  # python 3 need to use urllib.parse
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, fresh_login_required
import datetime
from itsdangerous import URLSafeSerializer

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///myDatabase.db"
app.config['SECRET_KEY'] = 'thisissecret'
app.config["USE_SESSION_FOR_NEXT"] = True
app.config["REMEMBER_COOKIE_DURATION"] = datetime.timedelta(minutes=1)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Redirect the user who is not authorized yet directly to the login page instead of the default Unauthorized page.
login_manager.login_view = "login"
login_manager.login_message = "You really need to login!"

# With fresh_login_required function, we can redirect them to another page, and send a message to let users know to re-login again.
login_manager.refresh_view = "login"
login_manager.needs_refresh_message = "You need to re-login to access this page!"

serializer = URLSafeSerializer(app.secret_key)


# UserMixin provides extra functions like is_authenticated, is_active, is_anonymous, get_id() ...etc.
class User(UserMixin, db.Model):
    # UserMixin's get_id() function limits the name of the primary column has to be "id"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    session_token = db.Column(db.String(100), unique=True)

    def get_id(self):
        return unicode(self.session_token)

# The more simple version
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

@login_manager.user_loader
def load_user(session_token):
    return User.query.filter_by(session_token=session_token).first()


def create_user():
    _username = "Leamon"
    _password = "password"
    user = User(username=_username, password=_password, session_token=serializer.dumps([_username, _password]))
    db.session.add(user)
    db.session.commit()


def update_token():
    _username = "Leamon"
    user = User.query.filter_by(username=_username).first()
    _newPassword = "newPassword"
    user.session_token = serializer.dumps([_username, _newPassword])
    db.session.commit()

@app.route("/")
def index():
    return "Home Page!"


@app.route("/login")
def login():
    session["next"] = request.args.get("next")
    # user = User.query.filter_by(username="Anthony").first()
    # login_user(user)
    # return "You are now logged in!"
    return render_template("login.html")

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and \
            ref_url.netloc == test_url.netloc

@app.route("/logmein", methods=["POST"])
def logmein():
    username = request.form["username"]
    user = User.query.filter_by(username=username).first()
    if not user:
        return "<h1>User not found!</h1>"
    
    # The parameter rememebr set to True meaning "rememebr me" function
    # Can set the expiration time by setting the parameter in the app.config
    login_user(user, remember=True)
    if "next" in session:
        next = session["next"]
        if is_safe_url(next) and next is not None:
            return redirect(next)

    return "You are now logged in!"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "You are now logged out!"

@app.route("/home")
@login_required
def home():
    return "The current user is " + current_user.username


@app.route("/fresh")
@fresh_login_required
def fresh_login_requiredPage():
    return "<h1>You have a fresh login!</h1>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)