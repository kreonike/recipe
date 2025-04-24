import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger
from faker import Faker

from models import Client, Parking

fake = Faker()


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = FuzzyChoice(
        [
            None,
            fake.credit_card_number(card_type='visa'),
            fake.credit_card_number(card_type='mastercard'),
        ]
    )
    car_number = factory.LazyFunction(
        lambda: fake.license_plate().replace('-', '').upper()
    )


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session_persistence = 'commit'

    address = factory.Faker('address')
    opened = FuzzyChoice([True, False])
    count_places = FuzzyInteger(5, 100)
    count_available_places = factory.LazyAttribute(
        lambda o: o.count_places if o.opened else 0
    )
