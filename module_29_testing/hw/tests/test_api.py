import pytest
from models import Client, Parking


@pytest.mark.parametrize(
    "route,expected",
    [
        ("/clients", 200),
        pytest.param(
            "/clients/1",
            200,
            marks=pytest.mark.xfail(reason="Requires existing client"),
        ),
    ],
)
def test_get_methods(client, route, expected):
    response = client.get(route)
    assert response.status_code == expected


def test_create_client(client, session):
    data = {"name": "New", "surname": "Client", "credit_card": "1111222233334444"}
    response = client.post("/clients", json=data)
    assert response.status_code == 201
    assert session.query(Client).count() == 2


def test_create_parking(client, session):
    data = {"address": "New Parking", "count_places": 20}
    response = client.post("/parkings", json=data)
    assert response.status_code == 201
    assert session.query(Parking).count() == 2


@pytest.mark.parking
def test_enter_parking(client, session):
    # Сначала создаем клиента
    client_data = {"name": "Parking", "surname": "User"}
    client.post("/clients", json=client_data)

    parking_data = {"client_id": 2, "parking_id": 1}
    response = client.post("/client_parkings", json=parking_data)
    assert response.status_code == 200
    assert response.json['available_places'] == 9


@pytest.mark.parking
def test_exit_parking(client, session):
    # Сначала заезд
    parking_data = {"client_id": 1, "parking_id": 1}
    client.post("/client_parkings", json=parking_data)

    # Затем выезд
    response = client.delete("/client_parkings", json=parking_data)
    assert response.status_code == 200
    assert response.json['available_places'] == 10
