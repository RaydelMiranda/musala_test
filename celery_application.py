import datetime
import os

from celery import Celery

from model.db import db_connection
from model.drone import DroneController

app = Celery()
app.conf.broker_url = 'redis://localhost:6379/0'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, check_drone_battery.s(), name='Check drone batteries.')


@app.task
def check_drone_battery():
    drones = DroneController.get_drone_list()
    if drones:
        data = []
        for drone in drones:
            data.append({
                'drone_serial_number': drone['serial'],
                'battery_level': drone['battery'],
                'time': datetime.datetime.utcnow().isoformat()
            })

        with db_connection("musala_test", "battery_logs") as battery_logs:
            battery_logs.insert_many(data)
