from flask import Flask, request, make_response
from functools import wraps

app = Flask(__name__)

def auth_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == "username2" and auth.password == "password":
            return func(*args, **kwargs)

        return make_response("Could not verify", 401, {"WWW-Authenticate": "Basic realm='Login Required'"})
    return decorated

@app.route("/")
def index():
    # request.authorization.username
    # request.authorization.password
    if request.authorization and request.authorization.username == "username" and request.authorization.password == "password":
        return "<h1>You are logged in!</h1>"

    return make_response("Could not verify", 401, {"WWW-Authenticate": "Basic realm='Login Required'"})

@app.route("/page1")
def page1():
    return "<h1>You are now on the page1!</h1>"

@app.route("/page2")
@auth_required
def page2():
    return "<h1>You are now on the page2!</h1>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)