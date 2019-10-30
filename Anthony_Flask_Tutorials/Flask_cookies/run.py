from flask import Flask, make_response, request

app = Flask(__name__)

@app.route("/setcookie")
def setcookie():
    resp = make_response("Setting cookie!")
    resp.set_cookie("framework", "flask")
    return resp

@app.route("/getcookie")
def getcookie():
    framework = request.cookies.get("framework")
    return "The framework is " + framework


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)