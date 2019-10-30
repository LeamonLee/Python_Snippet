from flask import Flask, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    session["user"] = "Anthony"
    return "Index"

@app.route("/getsession")
def getsession():
    if "user" in session:
        return session["user"]
    
    return "Not logged in!"

@app.route("/dropsession")
def dropsession():
    session.pop("user", None)
    return "Dropped!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)