import pytest
from app import create_app
from models import db, Client, Parking


@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()

        # Тестовые данные
        client = Client(name="Test", surname="User", credit_card="1234123412341234")
        parking = Parking(
            address="Test Address",
            opened=True,
            count_places=10,
            count_available_places=10,
        )
        db.session.add(client)
        db.session.add(parking)
        db.session.commit()

        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()


@pytest.fixture
def client_factory(session):
    from factories import ClientFactory

    ClientFactory._meta.sqlalchemy_session = session
    return ClientFactory


@pytest.fixture
def parking_factory(session):
    from factories import ParkingFactory

    ParkingFactory._meta.sqlalchemy_session = session
    return ParkingFactory
