from datetime import datetime

from flask import Flask, request, jsonify

from models import db, Client, Parking, ClientParking


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/clients', methods=['GET'])
    def get_clients():
        clients = Client.query.all()
        return jsonify([c.to_dict() for c in clients])

    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client(client_id):
        client = Client.query.get_or_404(client_id)
        return jsonify(client.to_dict())

    @app.route('/clients', methods=['POST'])
    def create_client():
        data = request.json
        client = Client(
            name=data['name'],
            surname=data['surname'],
            credit_card=data.get('credit_card'),
            car_number=data.get('car_number'),
        )
        db.session.add(client)
        db.session.commit()
        return jsonify({'message': 'Client created', 'id': client.id}), 201

    @app.route('/parkings', methods=['POST'])
    def create_parking():
        data = request.json
        parking = Parking(
            address=data['address'],
            opened=data.get('opened', True),
            count_places=data['count_places'],
            count_available_places=data['count_places'],
        )
        db.session.add(parking)
        db.session.commit()
        return jsonify({'message': 'Parking created', 'id': parking.id}), 201

    @app.route('/client_parkings', methods=['POST'])
    def enter_parking():
        data = request.json
        client = Client.query.get_or_404(data['client_id'])
        parking = Parking.query.get_or_404(data['parking_id'])

        if not parking.opened:
            return jsonify({'error': 'Parking is closed'}), 400

        if parking.count_available_places <= 0:
            return jsonify({'error': 'No available places'}), 400

        existing = ClientParking.query.filter_by(
            client_id=client.id, parking_id=parking.id, time_out=None
        ).first()

        if existing:
            return jsonify({'error': 'Client already on this parking'}), 400

        parking.count_available_places -= 1
        log = ClientParking(
            client_id=client.id, parking_id=parking.id, time_in=datetime.now()
        )
        db.session.add(log)
        db.session.commit()

        return (
            jsonify(
                {
                    'message': 'Client entered parking',
                    'available_places': parking.count_available_places,
                }
            ),
            200,
        )

    @app.route('/client_parkings', methods=['DELETE'])
    def exit_parking():
        data = request.json
        client = Client.query.get_or_404(data['client_id'])
        parking = Parking.query.get_or_404(data['parking_id'])

        log = ClientParking.query.filter_by(
            client_id=client.id, parking_id=parking.id, time_out=None
        ).first_or_404()

        if not client.credit_card:
            return jsonify({'error': 'No credit card assigned to client'}), 400

        parking.count_available_places += 1
        log.time_out = datetime.now()
        db.session.commit()

        return (
            jsonify(
                {
                    'message': 'Client exited parking',
                    'time_in': log.time_in.isoformat(),
                    'time_out': log.time_out.isoformat(),
                    'available_places': parking.count_available_places,
                }
            ),
            200,
        )

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
