from json.decoder import JSONDecodeError
from flask import Flask, request
from flask_restful import Resource, Api
from models import Person

app = Flask(__name__)
api = Api(app)


class ListCreatePerson(Resource):
    def post(self):
        try:
            data = request.json
            new_person = Person(name=data["name"], age=data["age"])
            new_person.save()

            return new_person.as_dict()

        except JSONDecodeError:
            return {
                "error": "Object a json serializeble",
                "message": "Object sended not a json!",
            }, 400

    def get(self):
        try:
            people = Person.query.all()
            data = []
            for p in people:
                data.append(p.as_dict())

            return data

        except Exception:
            response = {"status": "error", "message": "Cannot get all People"}
            return response, 400


class Persons(Resource):
    def get(self, name):
        try:
            person = Person.query.filter_by(name=name).first()
            return person.as_dict()
        except AttributeError:
            return {
                "error": "No object found",
                "message": "Person not found!",
            }, 404

    def put(self, name):
        try:
            person = Person.query.filter_by(name=name).first()
            data = request.json
            print(type(data))
            if not ("name" in data):
                raise AttributeError
            if not ("age" in data):
                raise AttributeError
            else:
                person.name = data["name"]
                person.age = data["age"]
                person.save()
                return person.as_dict(), 200
        except AttributeError:
            return {
                "error": "Attribute error",
                "message": "Some Attribute not found",
            }, 400

    def patch(self, name):
        try:
            person = Person.query.filter_by(name=name).first()
            new_person = request.json
            if "name" in new_person:
                person.name = new_person["name"]
            if "age" in new_person:
                person.age = new_person["age"]
                person.save()
                return person.as_dict()
        except Exception:
            return {"status": "error", "message": "Cannot patch Person"}, 400

    def delete(self, name):
        try:
            person = Person.query.filter_by(name=name).first()
            person.delete()
            return {
                "status": "sucess",
                "message": f"person with name '{name}' "
                "has deleted successfully",
            }

        except Exception:
            return {
                "status": "error",
                "message": "Some error has ocurred during delete!",
            }, 400


api.add_resource(Persons, "/person/<string:name>/")
api.add_resource(ListCreatePerson, "/person/")

if __name__ == "__main__":
    app.run(debug=True)
