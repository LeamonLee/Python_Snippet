from flask import Flask 
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

a_language = api.model('Language', {'language' : fields.String('The language.')}) #, 'id' : fields.Integer('ID')
 
languages = []
python = {'language' : 'Python', 'id' : 1}
languages.append(python)

@api.route('/language')
class Language(Resource):

    # With marshal_with decorator, flask-restplus will return only the fields you defined in the model instead of all the fields in raw source data.
    # envelop will make the output result data have a key-value pair and more like a JSON data. 
    @api.marshal_with(a_language, envelope='the_data')
    def get(self):
        return languages

    @api.expect(a_language)
    def post(self):
        new_language = api.payload 
        new_language['id'] = len(languages) + 1
        languages.append(new_language)
        return {'result' : 'Language added'}, 201 

if __name__ == '__main__':
    app.run(debug=True)