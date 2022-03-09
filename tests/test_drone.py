import base64

import pytest

from model.drone import *


class TestDrone:

    @pytest.mark.parametrize(
        "model,serial,weight,battery,state",
        [
            (DRONE_MODEL_LIGHT, "0" * 101, 500, 100, STATE_IDLE),  # Too long serial number.
            (DRONE_MODEL_LIGHT, "0", 501, 100, STATE_LOADING),  # Overweight.
            (DRONE_MODEL_LIGHT, "0", -1, 100, STATE_IDLE),  # Negative weight not allowed.
            (DRONE_MODEL_LIGHT, "0", 250, 101, STATE_IDLE),  # Battery values are in percentage can't be over 100.
            (DRONE_MODEL_LIGHT, "0", 300, -1, STATE_IDLE),  # Battery values are in percentage can't be negative.
            (DRONE_MODEL_LIGHT, "0", 300, 100, -1),  # Unknown state.
            (-1, "0", 300, 100, STATE_IDLE)  # Unknown model.
        ]
    )
    def test_drone_registration_requirements(self, model, serial, weight, battery, state):
        drone = Drone(model, serial, weight, battery, state)
        with pytest.raises(Exception):
            DroneController.register(drone)

    def test_drone_registration(self):
        # drone = Drone(DRONE_MODEL_LIGHT, '1234', 400, 50, STATE_IDLE | STATE_LOADED)
        drone = Drone(model=DRONE_MODEL_LIGHT, serial='1234',
                      max_weight=400, battery=50, state=STATE_IDLE | STATE_LOADED,
                      total_weight=0, meds=[])

        drone_id = DroneController.register(drone)

        with db_connection(os.environ['DB_NAME'], DRONES_COLLECTION_NAME) as drones:
            result = drones.find_one({"_id": drone_id})
            result.pop('_id')

        assert drone == Drone(**result)

    def test_drone_registration_no_dup_serial(self):
        drone_0 = Drone(DRONE_MODEL_LIGHT, '1234', 400, 50, STATE_IDLE | STATE_LOADED)
        drone_1 = Drone(DRONE_MODEL_HEAVY, '1234', 300, 30, STATE_IDLE)

        DroneController.register(drone_0)

        with pytest.raises(Exception):
            # Should not allow to dup serial numbers.
            DroneController.register(drone_1)

    def test_load_the_drone(self, drone):
        drone_id = DroneController.register(drone)

        med = Medication("C Vitamin", 500, 'VC', base64.b64encode("example".encode()))
        DroneController.load_drone(drone, med)

        # Get the drone from the db and check is correctly loaded.
        loaded_drone = DroneController.get_drone(drone.serial)

        assert loaded_drone.meds
        assert loaded_drone.total_weight == 500
        assert loaded_drone.meds[0].name == "C Vitamin"

        # Trying to add more to this same drone should fail.
        with pytest.raises(DroneOverweight):
            DroneController.load_drone(loaded_drone, med)

    def test_check_for_loading(self, drone):

        # Some random meds.
        med_0 = Medication("Some med", 500, "code", base64.b64encode("image".encode()))
        med_1 = Medication("Some med", 200, "code", base64.b64encode("image".encode()))
        # Some drones.
        drone_0 = drone = Drone(DRONE_MODEL_LIGHT, '1234', 500, 50, STATE_IDLE)
        drone_1 = drone = Drone(DRONE_MODEL_LIGHT, '6789', 400, 50, STATE_IDLE)
        drone_2 = drone = Drone(DRONE_MODEL_LIGHT, 'aa334', 500, 50, STATE_IDLE)

        DroneController.register(drone_0)
        DroneController.register(drone_1)
        DroneController.register(drone_2)

        # Load the the first drone with the max capacity.
        DroneController.load_drone(drone_0, med_0)

        # Ask for drones available for load.
        result = DroneController.drones_for_loading()

        # Should return drones 1 and 2
        assert drone_1.serial == result[0][0]
        assert drone_2.serial == result[1][0]

        result = DroneController.drones_for_loading(med_1)

        # Still should return the drones 1 and 2
        assert drone_1.serial == result[0][0]
        assert drone_2.serial == result[1][0]

        result = DroneController.drones_for_loading(med_0)

        # Only drone_2 has capacity for med_0
        assert len(result) == 1
        assert drone_2.serial == result[0][0]

    def test_battery_threshold(self, drone):
        drone.battery = 24
        med = Medication("C Vitamin", 500, 'VC', base64.b64encode("example".encode()))

        # Should except since battery is lower thant BATTERY_LOADING_THRESHOLD (25).
        with pytest.raises(LowBatteryError):
            DroneController.load_drone(drone, med)
