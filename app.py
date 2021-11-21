from json.decoder import JSONDecodeError
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

developers = [
    {"id": 1, "name": "Felipe", "skills": ["Python", "Flask"]},
    {"id": 2, "name": "Cassiemiro", "skills": ["Python", "Django"]},
]


@app.route("/developer/", methods=["GET", "POST"])
def developer():
    if request.method == "GET":
        try:
            return jsonify(developers), 200

        except Exception:
            response = {"status": "error", "message": "Cannot get all devs"}
            return response, 400

    elif request.method == "POST":
        try:
            new_developer = json.loads(request.data)
            developers_len = len(developers)
            new_developer["id"] = developers_len + 1
            developers.append(new_developer)

            return jsonify(new_developer), 201

        except JSONDecodeError:
            response = {
                "status": "error",
                "message": "Please make sure that payload is a JSON format",
            }
            return response, 400

        except Exception:
            response = {
                "status": "error",
                "message": "Cannot create new developer - Generic error!",
            }
            return response, 400


@app.route("/developer/<int:id>/", methods=["GET", "PUT", "DELETE"])
def developer_by_id(id):
    id -= 1
    if request.method == "GET":
        try:
            response = developers[id]
            return jsonify(response), 200

        except IndexError:
            response = {
                "status": "error",
                "message": f"Developer with ID {id} not exist!",
            }
            return response, 404

        except Exception:
            response = {"status": "error", "message": "Generic Error!"}
            return response, 400

    elif request.method == "PUT":
        try:
            payload = json.loads(request.data)
            payload["id"] = id + 1
            developers[id] = payload
            return jsonify(payload), 202

        except JSONDecodeError:
            response = {
                "status": "error",
                "message": "Please make sure that payload is a JSON format",
            }
            return response, 400
        except IndexError:
            response = {
                "status": "error",
                "message": f"Developer with ID {id} not exist!",
            }
            return response, 404

        except Exception:
            response = {"status": "error", "message": "Generic Error!"}
            return response, 400

    elif request.method == "DELETE":
        try:
            developers.pop(id)
            return (
                jsonify({"status": "sucess", "message": "Dev deleted!"}),
                204,
            )
        except Exception:
            response = {"status": "error", "message": "Generic Error!"}
            return response, 400


if __name__ == "__main__":
    app.run(debug=True)
