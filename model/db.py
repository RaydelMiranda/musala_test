import os
import pymongo
from contextlib import contextmanager

from logger_helper.drone_logger import musala_logger

DRONES_COLLECTION_NAME = 'drones'

drone_validation = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['model', 'serial', 'max_weight', 'state', 'battery'],
        'properties': {
            'model': {
                'bsonType': 'int',
                'minimum': 0,
                'maximum': 3,
                'description': "must be an integer and is required."
            },
            'serial': {
                'bsonType': 'string',
                'maxLength': 100,
                'description': "A string with no more than 100 characters, required."
            },
            'max_weight': {
                'bsonType': 'int',
                'minimum': 0,
                'maximum': 500,
                'description': "Weight this drone can carry, max 500."
            },
            'state': {
                'bsonType': 'int',
                'minimum': 0,
                'description': "A required integer representing the drone state."
            },
            'total_weight': {
                'bsonType': 'int',
                'description': "Total weight"
            },
            'battery': {
                'bsonType': 'int',
                'minimum': 0,
                'maximum': 100,
                'description': "Battery percentage"
            }
        }
    }
}


def add_validations():
    """
    If collection are going to be created by first time, add validations
    """
    client = pymongo.MongoClient(os.environ.get('MONGO_URL', 'localhost:27017'))
    db = client.get_database(os.environ['DB_NAME'])
    collection_names = db.list_collection_names()

    if DRONES_COLLECTION_NAME not in collection_names:
        # Create collection and add validations.
        db.create_collection(DRONES_COLLECTION_NAME)
        db.command('collMod', DRONES_COLLECTION_NAME, validator=drone_validation)

    client.close()


@contextmanager
def db_connection(db_name, collection):

    try:
        add_validations()
    except Exception as err:
        # If validation can't be added, log about it and continue, no validations
        # should not be a system braking issue.
        musala_logger.warning(f"Fail to add some validations: {err}")

    try:
        client = pymongo.MongoClient(os.environ.get('MONGO_URL', 'localhost:27017'))
        db = client.get_database(db_name)
        collection = db.get_collection(collection)
        yield collection
    except Exception as err:
        raise err
    else:
        client.close()


