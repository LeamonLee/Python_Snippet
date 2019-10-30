from flask import Flask 
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

# The first argument is to specify the model name.
a_language = api.model('Language_Model', {'language' : fields.String('Please type in a language you want.')})

languages = []
python = {'language' : 'Python'}
languages.append(python)

@api.route('/language')
class Language(Resource):
    def get(self):
        # return {"Hello", "restplus"}      # no need to use jsonify like regular flask API in here.
        return languages

    @api.expect(a_language)
    def post(self):
        languages.append(api.payload)
        return {'result' : 'Language added'}, 201 

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)