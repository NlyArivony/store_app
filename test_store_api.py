import requests

ENDPOINT = "http://localhost:5000/"


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    pass


def test_get_stores():
    response = requests.get(f"{ENDPOINT}/store")
    assert response.status_code == 200
    pass


def test_get_one_specific_store():
    store_name = "my store"
    response = requests.get(f"{ENDPOINT}/store/{store_name}")
    assert response.status_code == 200
    pass


def test_create_store():
    payload = {"name": "test", "items": [{"name": "Table", "price": 25.99}]}
    response = requests.post(f"{ENDPOINT}/store", json=payload)
    assert response.status_code == 201


def test_create_item_in_a_store():
    store_name = "test"
    payload = {"name": "TV", "price": 100}
    response = requests.post(f"{ENDPOINT}/store/{store_name}/item", json=payload)
    assert response.status_code == 201
