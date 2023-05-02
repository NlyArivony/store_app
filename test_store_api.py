import requests

ENDPOINT = "http://localhost:5005/"


# def test_can_call_endpoint():
#     response = requests.get(ENDPOINT)
#     assert response.status_code == 200
#     pass


def test_get_stores():
    response = requests.get(f"{ENDPOINT}/store")
    assert response.status_code == 200
    pass


def test_get_items():
    response = requests.get(f"{ENDPOINT}/item")
    assert response.status_code == 200
    pass


def test_create_store():
    payload = {"name": "store 1"}
    response = requests.post(f"{ENDPOINT}/store", json=payload)
    assert response.status_code == 201


def test_create_item():
    payload = {"name": "store 2"}
    response = requests.post(f"{ENDPOINT}/store", json=payload)
    assert response.status_code == 201


def test_create_item():
    payload = {"name": "store 2"}
    response = requests.post(f"{ENDPOINT}/store", json=payload)
    assert response.status_code == 201
    store_data = response.json()
    store_id = store_data["id"]
    payload = {"store_id": store_id, "price": 105, "name": "Tv"}
    response = requests.post(f"{ENDPOINT}/item", json=payload)
    assert response.status_code == 201


def test_delete_item_and_store():
    store_payload = {"name": "store 3 to be deleted"}
    store_response = requests.post(f"{ENDPOINT}/store", json=store_payload)
    assert store_response.status_code == 201
    store_data = store_response.json()

    store_id = store_data["id"]
    item_payload = {"store_id": store_id, "price": 10, "name": "item to be deleted"}
    item_response = requests.post(f"{ENDPOINT}/item", json=item_payload)
    assert item_response.status_code == 201
    item_data = item_response.json()

    item_id = item_data["id"]
    delete_item_response = requests.delete(f"{ENDPOINT}/item/{item_id}")
    assert delete_item_response.status_code == 200

    delete_store_response = requests.delete(f"{ENDPOINT}/store/{store_id}")
    assert delete_store_response.status_code == 200


def test_update_item():
    store_payload = {"name": "store 4 to be updated"}
    store_response = requests.post(f"{ENDPOINT}/store", json=store_payload)
    assert store_response.status_code == 201
    store_data = store_response.json()

    store_id = store_data["id"]
    item_payload = {"store_id": store_id, "price": 10, "name": "item to be updated"}
    item_response = requests.post(f"{ENDPOINT}/item", json=item_payload)
    assert item_response.status_code == 201
    item_data = item_response.json()

    item_id = item_data["id"]
    updated_item_payload = {"price": 15, "name": "item updated"}
    updated_item_response = requests.put(
        f"{ENDPOINT}/item/{item_id}", json=updated_item_payload
    )
    assert updated_item_response.status_code == 200


# if __name__ == "__main__":
#     test_update_item()
