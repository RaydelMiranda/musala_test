from flask import Flask
from flask_restful import Resource, Api

from resources.drone import Drone


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Drone, '/drones/')

    return app


if __name__ == '__main__':
    # Debug activated by default for testing purpose only.
    create_app().run(debug=True)
