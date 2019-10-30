from flask import Flask, jsonify, request
app = Flask(__name__)

languages = [{"name": "Javascript"}, {"name": "Python"}, {"name": "Ruby"}]

@app.route("/", methods=["GET"])
def test():
    return jsonify({"message": "API works"})


@app.route("/languages", methods=["GET"])
def returnAll():
    return jsonify({"languages": languages})


@app.route("/languages/<string:name>", methods=["GET"])
def returnOne(name):
    _langs = [language for language in languages if language["name"] == name]
    return jsonify({"language": _langs[0]})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)