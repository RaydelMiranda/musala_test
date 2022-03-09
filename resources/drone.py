from dataclasses import asdict

from flask import request, jsonify
from flask_restful import Resource

from model.drone import DroneController, Drone as DroneModel, DroneNotFound, DroneOverweight, LowBatteryError
from model.meds import Medication


class Drone(Resource):

    def post(self):
        json_data = request.json
        drone = DroneModel(**json_data)
        return {"id": DroneController.register(drone)}, 201

    def get(self):
        return DroneController.get_drone_list(), 200


class SingleDrone(Resource):

    def get(self, serial):
        try:
            result = DroneController.get_drone(serial)
        except DroneNotFound as err:
            return {'err': str(err)}, 404
        else:
            return asdict(result), 200


class DroneLoader(Resource):

    def post(self, serial):

        json_data = request.json

        if not isinstance(json_data, list):
            return {'err': "Meds has to be provided as an array"}, 400

        meds = [Medication(**data) for data in json_data]

        try:
            drone = DroneController.get_drone(serial)
        except DroneNotFound as err:
            return {'err': str(err)}, 404

        total_weight = drone.total_weight

        try:
            # TODO: For optimization purposes, adding more than one
            # med to a single drone should be carried using only one
            # db query.
            for med in meds:
                total_weight += DroneController.load_drone(drone, med)
        except DroneOverweight as err:
            return {'err': str(err), 'total_weight': total_weight}, 409
        except LowBatteryError as err:
            return {'err': str(err)}, 409
        else:
            return {'updated_current_weight': total_weight}, 200


class DronesAvailableForLoad(Resource):

    def get(self):
        data = request.json
        med = None
        if data:
            med = Medication(**data)
        result = DroneController.drones_for_loading(med)

        return {'data': result}, 200
