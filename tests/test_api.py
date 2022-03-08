import base64

from model.drone import DRONE_MODEL_HEAVY, DroneController


class TestApi:

    def test_drone_registration(self, client):
        response = client.post('/drones/', json={
            'model': DRONE_MODEL_HEAVY,
            'serial': '00000',
            'max_weight': 300
        })

        response.status_code = 201
        assert response.json == {'id': '00000'}

    def test_get_all_drones(self, client, drone):
        DroneController.register(drone)
        response = client.get('/drones/')
        assert response.status_code == 200

    def test_get_drone(self, client, drone):
        # Asking for a drone that has not been registered.
        response = client.get(f'/drone/{drone.serial}/')
        assert response.status_code == 404

        DroneController.register(drone)
        response = client.get(f'/drone/{drone.serial}/')
        assert response.status_code == 200

    def test_load_drone(self, client, drone):
        data = [{
            'name': "C Vitamin",
            'weight': 500,
            'code': 'VC',
            'image': str(base64.b64encode("example".encode()))
        }]
        DroneController.register(drone)
        response = client.post(f'/drone/load/{drone.serial}/', json=data)

        assert response.status_code == 200