from marshmallow import Schema, fields, pprint, post_load, ValidationError, validates

class Person(object):
    def __init__(self, name, age, email):
        self.name = name 
        self.age = age
        self.email = email 

    def __repr__(self):
        return '{} is {} years old'.format(self.name, self.age)

def validate_age(age):
    print("2")
    if age < 25:
        print("3")
        # return False
        raise ValidationError("Please enter the age above 25")


class PersonSchema(Schema):
    name = fields.String()
    age = fields.Integer(validate=validate_age)
    email = fields.Email()
    # location = fields.String(required=True)               # Must type in this field if you specify required=True

    # Need to use @post_load to create a Person object, otherwise it will just return a simple data type.
    @post_load
    def create_person(self, data):
        return Person(**data)
    
    @validates("name")                          # Needs to pass in the field name in validates()
    def validate_nameLength(self, name):
        print("1")
        if len(name) < 5 or len(name) > 10:
            print("4")
            raise ValidationError("The length of name must be between 5~10 charactors.")


input_dict = {}

input_dict['name'] = input('What is your name? ')
input_dict['age'] = input('How old are you? ')
input_dict['email'] = input('What is your email? ')

person = Person(name=input_dict['name'], age=input_dict['age'], email=input_dict["email"])
print(person)

schema = PersonSchema()
result = schema.dump(person)           # serialize:     object(complex python data type) --> simple python data type
result2 = schema.load(input_dict)        # deserialize:   simple python data type --> object (complex python data type)

pprint(result.data)
pprint(result.errors)
pprint(result2.data)
pprint(result2.errors)
