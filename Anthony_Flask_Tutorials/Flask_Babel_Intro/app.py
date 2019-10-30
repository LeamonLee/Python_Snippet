from flask import Flask, render_template
from babel import numbers

app = Flask(__name__)


@app.route("/")
def index():

    us_num = numbers.format_decimal(1.2345, locale="en-US")
    num = numbers.format_decimal(1.2345, locale="en-US")
    results = {"num": num}
    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)