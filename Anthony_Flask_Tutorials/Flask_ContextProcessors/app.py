from flask import Flask, render_template, g, request


app = Flask(__name__)

@app.before_request
def before_request():
    print('before request started')
    if not hasattr(g,'prev'):
        setattr(g,'prev','before_request')

@app.before_request
def before_request2():
    print('before request started 2')
    print(request.url)
    g.name="SampleApp"

@app.after_request
def after_request(response):
    print('after request finished')
    print(request.url)
    response.headers['key'] = 'value'
    return response

@app.teardown_request
def teardown_request(exception):
    print('teardown request')
    print(request.url)


@app.route("/")
def index():
    g.prev = 'index'
    return render_template("index.html", key1="value1")

@app.route("/home")
def home():
    print("previous g.prev: ", g.prev)
    g.prev = 'home'
    return render_template("index.html", key1="value1")

@app.route("/about")
def about():
    print("previous g.prev: ", g.prev)
    g.prev = 'about'
    return render_template("index.html", key1="value1")

def returnString():
    return "Just A String"

# Need to return a dictionary
@app.context_processor
def myContextProcessor():
    return {
        "key2":"value2",
        "returnString": returnString
    }


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)