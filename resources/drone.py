from flask import request
from flask_restful import Resource

from model.drone import DroneController, Drone as DroneModel


class Drone(Resource):

    def post(self):
        json_data = request.json
        drone = DroneModel(**json_data)
        return {"id": DroneController.register(drone)}, 201


