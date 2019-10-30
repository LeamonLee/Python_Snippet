from flask import Flask

app = Flask(__name__)

request_state = ''

@app.before_request
def before_request():
    global request_state
    request_state += ' before_request'

# Must take in one response object, and need to return a response object.
# After_request only runs when the request was successful.
@app.after_request
def after_request(resp):
    global request_state
    request_state += ' after_request'
    return resp

# teardown_request always runs regardless of what happens in the requests
@app.teardown_request
def teardown_request(excep):
    global request_state
    request_state += ' teardown <br>'

@app.route('/')
def index():
    return 'Hello ' + request_state

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)