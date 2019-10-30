from flask import Flask
from os import environ

app = Flask(__name__)

# Need to export the environment variable in the command line first
# export APP_SETTINGS=config.cfg
app.config.from_envvar("APP_SETTINGS")

# export STRIPE_API_KEY=12345
app.config["STRIPE_API"] = environ.get("STRIPE_API_KEY")

@app.route("/")
def index():
    return "<h1>" + app.config["STRIPE_API"] + "</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)