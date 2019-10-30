from flask import Flask

app = Flask(__name__)

# DEBUG = True
DEBUG = False
app.config.from_object(__name__)
app.config.from_pyfile("myConfig.cfg")

@app.route('/')
def index():
    return "Hello There!"

if __name__ == "__main__":
    app.run()