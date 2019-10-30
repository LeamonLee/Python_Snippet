from flask import Flask, render_template, make_response
import pdfkit
import os


app = Flask(__name__)

# Example: http://127.0.0.1:5000/Anthony/Las Vegas
@app.route("/<name>/<location>")
def pdf_template(name, location):
    rendered = render_template("pdf_template.html", name=name, location=location)

    strCurrentPath = os.path.dirname(os.path.abspath(__file__))
    path_wkthmltopdf = strCurrentPath + r'\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    # pdfkit.from_url("http://google.com", "out.pdf", configuration=config)
    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    # response.headers["Content-Disposition"] = "attachment; filename=output.pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"

    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)