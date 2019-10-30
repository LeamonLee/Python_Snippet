from flask import Flask, request, make_response, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisisthesecretkey"


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # http://127.0.0.1:5000/route?token=kdjfkjuehaslks2847548skd
        token = request.args.get("token")
        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"message": "Token is invalid!"}), 403

        return func(*args, **kwargs)
    return decorated

@app.route("/")
def index():
    return "<h1>Home Page!</h1>"

@app.route("/unprotected")
def unprotected():
    return jsonify({"message": "Anyone can view this!"})


@app.route("/protected")
@token_required
def protected():
    return jsonify({"message": "This is available for people with valid tokens!"})

@app.route("/login")
def login():
    auth = request.authorization
    if auth and auth.password == "password":
        token = jwt.encode({"user": auth.username, 
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config["SECRET_KEY"])

        # Python3 needs to convert the bytes to string
        return jsonify({"token": token.decode("UTF-8")})

    return make_response("Could not verify!", 401, {"WWW-Authenticate": "Basic realm:'Login Required!'"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)