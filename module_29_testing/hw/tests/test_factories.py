import pytest
from models import Client, Parking


def test_client_creation_with_factory(client_factory, session):
    """Тест создания клиента с использованием фабрики"""
    initial_count = session.query(Client).count()

    client = client_factory()

    assert client.id is not None
    assert session.query(Client).count() == initial_count + 1
    assert isinstance(client.name, str)
    assert isinstance(client.surname, str)
    assert client.car_number is not None


def test_parking_creation_with_factory(parking_factory, session):
    """Тест создания парковки с использованием фабрики"""
    initial_count = session.query(Parking).count()

    parking = parking_factory()

    assert parking.id is not None
    assert session.query(Parking).count() == initial_count + 1
    assert isinstance(parking.address, str)
    assert isinstance(parking.count_places, int)
    assert parking.count_available_places in [0, parking.count_places]

    if parking.opened:
        assert parking.count_available_places == parking.count_places
    else:
        assert parking.count_available_places == 0


@pytest.mark.parametrize('count', [1, 3, 5])
def test_multiple_clients_creation(client_factory, session, count):
    """Тест создания нескольких клиентов"""
    initial_count = session.query(Client).count()

    clients = client_factory.create_batch(count)

    assert len(clients) == count
    assert session.query(Client).count() == initial_count + count
    assert all(client.id is not None for client in clients)
