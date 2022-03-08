"""
Note: python >=3.9 support enums which is a more suitable
structure for this.
"""
import logging
import os
from dataclasses import dataclass, asdict, field
from functools import reduce
from typing import List

from bson import ObjectId

from logger_helper.drone_logger import musala_logger
from model.db import db_connection, DRONES_COLLECTION_NAME
from model.meds import Medication

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
STATE_IDLE = 1
STATE_LOADING = 2
STATE_LOADED = 4
STATE_DELIVERING = 8
STATE_DELIVERED = 16
STATE_RETURNING = 32


class DroneError(Exception):
    pass


class DroneOverweight(DroneError):
    pass


@dataclass
class Drone:
    model: int
    serial: str
    weight: int
    battery: int = 0
    state: int = STATE_IDLE
    _id: any = field(init=False)
    meds: List[Medication] = field(default_factory=lambda: [])

    def __post_init__(self):
        self._id = self.serial

    def total_weight(self) -> int:
        if self.meds:
            total = reduce(
                lambda x, y: x + y,
                [med.weight for med in self.meds]
            )
        else:
            total = 0
        return total


class DroneController:

    @staticmethod
    def register(drone: Drone) -> ObjectId:
        with db_connection(os.environ.get('DB_NAME', 'musala_drones'), DRONES_COLLECTION_NAME) as drones_coll:
            try:
                post_id = drones_coll.insert_one(asdict(drone)).inserted_id
            except Exception as err:
                musala_logger.error(str(err))
                raise
            else:
                return post_id

    @staticmethod
    def load_drone(drone: Drone, med: Medication) -> int:
        """
        Load a drone with provided medication and return the total weight,
        raise DroneOverweight exception if weight limit is violated.
        """

        if drone.total_weight() + med.weight > drone.weight:
            raise DroneOverweight

        drone.meds.append(med)

        with db_connection(os.environ['DB_NAME'], DRONES_COLLECTION_NAME) as drones:
            try:
                drones.update_one({'serial': drone.serial}, {'$push': {'meds': asdict(med)}}, True)
            except Exception as err:
                musala_logger.error(err)

            drone.meds.append(med)
        return drone.total_weight()



