from flask import Flask
from flask_restful import Resource, Api

from resources.drone import Drone, SingleDrone, DroneLoader


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Drone, '/drones/')
    api.add_resource(SingleDrone, '/drone/<serial>/')
    api.add_resource(DroneLoader, '/drone/load/<serial>/')

    return app


if __name__ == '__main__':
    # Debug activated by default for testing purpose only.
    create_app().run(debug=True)
