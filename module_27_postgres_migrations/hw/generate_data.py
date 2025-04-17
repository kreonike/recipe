from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import db, Coffee, User
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/skillbox_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

RANDOM_NAMES = [
    "Alice Smith", "Bob Johnson", "Charlie Brown", "Diana Wilson", "Emma Davis",
    "Frank Miller", "Grace Taylor", "Henry Clark", "Isabella Lee", "James Moore"
]

session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429])
session.mount('https://', HTTPAdapter(max_retries=retries))

def wait_for_db():
    """Ожидание готовности базы данных"""
    max_retries = 10
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            with app.app_context():
                with db.engine.connect() as connection:
                    connection.execute(db.text('SELECT 1'))
                print('Database is ready!')
                return True
        except Exception as e:
            print(f'Database connection failed (attempt {attempt + 1}/{max_retries}): {e}')
            time.sleep(retry_delay)

    print('Failed to connect to database after multiple attempts')
    return False

def generate_test_data():
    """Генерация тестовых данных для таблиц coffee и users"""
    print('Starting generate_test_data...')
    if not wait_for_db():
        print('Failed to connect to database. Exiting generate_test_data.')
        return

    with app.app_context():
        print('Creating database tables...')
        db.create_all()

        try:
            if Coffee.query.count() > 0 or User.query.count() > 0:
                print('Data already exists in the database. Skipping generation.')
                return
        except Exception as e:
            print(f'Database query error: {e}')
            raise

        coffees = []
        for i in range(10):
            print(f'Generating coffee #{i + 1}...')
            try:
                response = session.get('https://random-data-api.com/api/coffee/random_coffee', timeout=5)
                response.raise_for_status()
                coffee_data = response.json()

                coffee = Coffee(
                    title=coffee_data.get('blend_name', f'Unknown Blend {i}'),
                    origin=coffee_data.get('origin', 'Unknown Origin'),
                    intensifier=coffee_data.get('intensifier', 'Unknown Intensifier'),
                    notes=coffee_data.get('notes', '').split(', ') if coffee_data.get('notes') else []
                )
                coffees.append(coffee)
                db.session.add(coffee)
            except (requests.RequestException, ValueError) as e:
                print(f'Error fetching coffee data: {e}')
                coffee = Coffee(
                    title=f'Backup Blend {i}',
                    origin='Unknown',
                    intensifier='Medium',
                    notes=['smooth', 'balanced']
                )
                coffees.append(coffee)
                db.session.add(coffee)
            time.sleep(1)

        try:
            db.session.commit()
            print(f'Successfully added {len(coffees)} coffee entries.')
        except Exception as e:
            print(f'Error committing coffee entries: {e}')
            db.session.rollback()
            raise

        for i in range(10):
            print(f"Generating user #{i + 1}...")
            try:
                response = session.get('https://random-data-api.com/api/address/random_address', timeout=5)
                response.raise_for_status()
                address_data = response.json()

                address = {
                    'street': address_data.get('street_name', '123 Main St'),
                    'city': address_data.get('city', 'Springfield'),
                    'country': address_data.get('country', 'USA'),
                    'zip_code': address_data.get('zip_code', '12345')
                }

                name = random.choice(RANDOM_NAMES)
                coffee = random.choice(coffees) if coffees else None

                user = User(
                    name=name,
                    surname=name.split()[-1],
                    patronomic=f'{name.split()[0]}ovich',
                    has_sale=random.choice([True, False]),
                    address=address,
                    coffee_id=coffee.id if coffee else None
                )
                db.session.add(user)
            except (requests.RequestException, ValueError) as e:
                print(f'Error fetching address data: {e}')
                name = random.choice(RANDOM_NAMES)
                user = User(
                    name=name,
                    surname=name.split()[-1],
                    patronomic=f'{name.split()[0]}ovich',
                    has_sale=False,
                    address={
                        'street': '123 Backup St',
                        'city': 'Default City',
                        'country': 'Default Country',
                        'zip_code': '00000'
                    },
                    coffee_id=random.choice(coffees).id if coffees else None
                )
                db.session.add(user)
            time.sleep(1)

        try:
            db.session.commit()
            print('Successfully added 10 user entries.')
        except Exception as e:
            print(f'Error committing user entries: {e}')
            db.session.rollback()
            raise

        print('Finished generate_test_data successfully.')

if __name__ == '__main__':
    try:
        print('Starting test data generation...')
        generate_test_data()
        print('Test data generation completed.')
    except Exception as e:
        print(f'Critical error in test data generation: {e}')
        raise