from json.decoder import JSONDecodeError
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy.sql.sqltypes import _AbstractInterval
from models import Activities, Person

app = Flask(__name__)
api = Api(app)


class ListCreatePerson(Resource):
    def post(self):
        try:
            data = request.json
            if data.get("name") and data.get("age"):
                new_person = Person(name=data["name"], age=data["age"])
                new_person.save()
            else:
                return {
                    "error": "KeyError",
                    "message": "Necessary all fields to create"
                    " person (name, age)",
                }, 400
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
                "error": "error",
                "message": "Person not found!",
            }, 404

    def put(self, name):
        try:
            person = Person.query.filter_by(name=name).first()
            data = request.json

            if not ("name" in data) or not ("age" in data):
                return {
                    "error": "KeyError",
                    "message": "Necessary all fields to update"
                    " person (name, age)",
                }, 400
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


class ListCreateActivities(Resource):
    def post(self):
        data = request.json
        person = Person.query.filter_by(name=data["person"]).first()
        if not person:
            return {
                "error": "not found",
                "message": f"Person with name {data['person']} not found",
            }, 404

        activity = Activities(name=data["name"], person=person)
        activity.save()
        return activity.as_dict()

    def get(self):
        activities = Activities.query.all()
        data = []
        for a in activities:
            data.append(a.as_dict())
        return data


api.add_resource(Persons, "/person/<string:name>/")
api.add_resource(ListCreatePerson, "/person/")
api.add_resource(ListCreateActivities, "/activity/")

if __name__ == "__main__":
    app.run(debug=True)
