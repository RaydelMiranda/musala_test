import pytest

from model.drone import *


class TestDrone:

    @pytest.mark.parametrize(
        "model,serial,weight,battery,state",
        [
            (DRONE_MODEL_LIGHT, "0"*101, 500, 100, STATE_IDLE),   # Too long serial number.
            (DRONE_MODEL_LIGHT, "0", 501, 100, STATE_LOADING),    # Overweight.
            (DRONE_MODEL_LIGHT, "0", -1, 100, STATE_IDLE),        # Negative weight not allowed.
            (DRONE_MODEL_LIGHT, "0", 250, 101, STATE_IDLE),       # Battery values are in percentage can't be over 100.
            (DRONE_MODEL_LIGHT, "0", 300, -1, STATE_IDLE),        # Battery values are in percentage can't be negative.
            (DRONE_MODEL_LIGHT, "0", 300, 100, -1),               # Unknown state.
            (-1, "0", 300, 100, STATE_IDLE)                       # Unknown model.
        ]
    )
    def test_drone_registration_requirements(self, model, serial, weight, battery, state):
        drone = Drone(model, serial, weight, battery, state)
        with pytest.raises(Exception):
            DroneController.register(drone)
