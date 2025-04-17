from flask import Flask, request, jsonify
from app.models import db, Coffee, User
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/skillbox_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/users', methods=['POST'])
def add_user():
    """Add a new user with optional coffee association."""
    data = request.get_json()

    # Validate required fields
    if not data or not isinstance(data, dict):
        return jsonify({'error': 'Invalid or missing JSON data'}), 400
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    if not data.get('address') or not isinstance(data.get('address'), dict):
        return jsonify({'error': 'Valid address (JSON object) is required'}), 400

    try:
        random_coffee = Coffee.query.order_by(func.random()).first()

        new_user = User(
            name=data.get('name'),
            surname=data.get('surname', ''),
            patronomic=data.get('patronomic', ''),
            has_sale=data.get('has_sale', False),
            address=data.get('address'),
            coffee_id=random_coffee.id if random_coffee else None
        )

        db.session.add(new_user)
        db.session.commit()

        coffee_data = None
        if new_user.coffee:
            coffee_data = {
                'id': new_user.coffee.id,
                'title': new_user.coffee.title,
                'origin': new_user.coffee.origin
            }

        return jsonify({
            'id': new_user.id,
            'name': new_user.name,
            'surname': new_user.surname,
            'patronomic': new_user.patronomic,
            'has_sale': new_user.has_sale,
            'address': new_user.address,
            'coffee': coffee_data
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@app.route('/coffees/search')
def search_coffee():
    """Search coffees by title."""
    query = request.args.get('query', '')

    coffees = Coffee.query.filter(
        Coffee.title.ilike(f'%{query}%')
    ).all()

    if not coffees:
        return jsonify({'message': 'No coffees found', 'results': []}), 200

    return jsonify([{
        'id': coffee.id,
        'title': coffee.title,
        'origin': coffee.origin,
        'intensifier': coffee.intensifier
    } for coffee in coffees])


@app.route('/coffees/notes')
def get_unique_notes():
    """Get unique coffee notes."""
    all_notes = db.session.query(
        func.unnest(Coffee.notes).label('note')
    ).distinct().all()

    unique_notes = [note[0] for note in all_notes if note[0]]

    if not unique_notes:
        return jsonify({'message': 'No notes found', 'notes': []}), 200

    return jsonify(unique_notes)


@app.route('/users/by_country')
def get_users_by_country():
    """Get users filtered by country."""
    country = request.args.get('country', '')

    if not country:
        return jsonify({'error': 'Country parameter is required'}), 400

    try:
        users = User.query.filter(
            User.address['country'].astext.ilike(f'%{country}%')
        ).all()

        if not users:
            return jsonify({'message': 'No users found', 'results': []}), 200

        return jsonify([{
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'patronomic': user.patronomic,
            'country': user.address.get('country') if user.address else None,
            'coffee': {
                'title': user.coffee.title if user.coffee else None
            }
        } for user in users])

    except KeyError:
        return jsonify({'error': 'Invalid address format in database'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)