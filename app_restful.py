from flask import Flask, request
from flask_restful import Resource, Api
from json.decoder import JSONDecodeError
import json

app = Flask(__name__)
api = Api(app)


developers = [
    {
        'id': 1,
        'name': 'Felipe',
        'skills': ['Python', 'Flask']
    },
    {
        'id': 2,
        'name': 'Gilena',
        'skills': ['Python', 'Django']
    }
]

class Developer(Resource):
    def get(self, id):
        id -= 1
        try:
            response = developers[id]
            return response, 200

        except IndexError:
            index = id + 1
            response = {
                'status': 'error',
                'message': f'Developer with ID {index} not exist!'
            }
            return response, 404

        except Exception:
            response = {
                'status': 'error',
                'message': 'Generic Error!'
            }
            return response, 400

    def put(self, id):
        id -= 1
        put_dev = json.loads(request.data)
        developers[id] = put_dev
        return put_dev


    def delete(self, id):
        id -= 1
        try:
            developers.pop(id)
            return {
                    'status': 'sucess',
                    'message': 'Dev deleted!'
                }, 204
        except IndexError:
            index = id + 1
            response = {
                'status': 'error',
                'message': f'Developer with ID {index} not exist!'
            }
            return response, 400


class ListCreateDeveloper(Resource):
    def get(self):
        try:
            return developers, 200

        except Exception:
            response = {
                'status': 'error',
                'message': 'Cannot get all devs'
            }
            return response, 400

    def post(self):
        try:
            new_developer = json.loads(request.data)
            developers_len = len(developers)
            new_developer['id'] = developers_len + 1
            developers.append(new_developer)

            return new_developer, 201

        except JSONDecodeError:
            response = {
                'status': 'error',
                'message': 'Please make sure that payload is a JSON format'
            }
            return response, 400


api.add_resource(ListCreateDeveloper, '/developer/')
api.add_resource(Developer, '/developer/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True)
