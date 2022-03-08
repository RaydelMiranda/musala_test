"""
Note: python >=3.9 support enums which is a more suitable
structure for this.
"""
import logging
import os
from dataclasses import dataclass, asdict

from bson import ObjectId

from logger_helper.drone_logger import musala_logger
from model.db import db_connection

logger = logging.getLogger(__name__)

DRONE_MODEL_LIGHT = 0
DRONE_MODEL_MIDDLE = 1
DRONE_MODEL_CRUISE = 2
DRONE_MODEL_HEAVY = 3

"""
Here I am going to use the flag technique, since
from my point of view a drone can and will have
more than one state often. For instance a drone should will be loaded while
delivering if not, the drone has gone without being loaded.
"""
STATE_IDLE = 0
STATE_LOADING = 1
STATE_LOADED = 2
STATE_DELIVERING = 4
STATE_DELIVERED = 8
STATE_RETURNING = 16


@dataclass
class Drone:
    model: int
    serial: str
    weight: int
    battery: int = 0
    state: int = STATE_IDLE


class DroneController:

    @staticmethod
    def register(drone: Drone) -> ObjectId:
        with db_connection(os.environ.get('DB_NAME', 'musala_drones'), 'drones') as drones_coll:
            try:
                post_id = drones_coll.insert_one(asdict(drone)).inserted_id
            except Exception as err:
                musala_logger.error(str(err))
                raise
            else:
                return post_id
