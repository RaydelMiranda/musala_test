from model.drone import DRONE_MODEL_HEAVY


class TestApi:

    def test_drone_registration(self, client):
        response = client.post('/drones/', json={
            'model': DRONE_MODEL_HEAVY,
            'serial': '00000',
            'max_weight': 300
        })

        response.status_code = 201
        assert response.json == {'id': '00000'}