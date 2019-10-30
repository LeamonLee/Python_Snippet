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


@app.route("/languages", methods=["POST"])
def addOne():
    language = {"name": request.json["name"]}

    languages.append(language)
    return jsonify({"languages": languages})

@app.route("/languages/<string:name>", methods=["PUT"])
def editOne(name):
    _langs = [language for language in languages if language["name"] == name]
    _langs[0]["name"] = request.json["name"]
    return jsonify({"language": _langs[0]})


@app.route("/languages/<string:name>", methods=["DELETE"])
def removeOne(name):
    _langs = [language for language in languages if language["name"] == name]
    languages.remove(_langs[0])
    return jsonify({"languages": languages})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)