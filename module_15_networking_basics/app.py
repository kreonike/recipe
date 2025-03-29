from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/booking": {"origins": "*", "methods": ["POST", "OPTIONS"]}})

rooms = []
bookings = []


def is_room_available(room_id, check_in, check_out):
    """Проверка доступности комнаты"""
    try:
        check_in_date = datetime.strptime(str(check_in), "%Y%m%d").date()
        check_out_date = datetime.strptime(str(check_out), "%Y%m%d").date()

        for booking in bookings:
            if booking['roomId'] == room_id:
                existing_check_in = datetime.strptime(
                    str(booking['bookingDates']['checkIn']), "%Y%m%d"
                ).date()
                existing_check_out = datetime.strptime(
                    str(booking['bookingDates']['checkOut']), "%Y%m%d"
                ).date()

                if not (
                    check_out_date <= existing_check_in
                    or check_in_date >= existing_check_out
                ):
                    return False
        return True
    except Exception:
        return False


@app.route('/add-room', methods=['POST'])
def add_room():
    """Добавление новой комнаты"""
    try:
        data = request.get_json()

        required_fields = ['floor', 'beds', 'guestNum', 'price']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        room_id = max(room['roomId'] for room in rooms) + 1 if rooms else 1
        new_room = {
            'roomId': room_id,
            'floor': data['floor'],
            'beds': data['beds'],
            'guestNum': data['guestNum'],
            'price': data['price'],
        }

        rooms.append(new_room)
        return jsonify({"message": "Room added successfully", "roomId": room_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/room', methods=['GET'])
def get_rooms():
    """Получение списка доступных комнат"""
    try:
        check_in = request.args.get('checkIn', '20210101')
        check_out = request.args.get('checkOut', '20211231')
        guests_num = int(request.args.get('guestsNum', 1))

        available_rooms = [
            room
            for room in rooms
            if (
                room['guestNum'] >= guests_num
                and is_room_available(room['roomId'], check_in, check_out)
            )
        ]

        return jsonify({"rooms": available_rooms}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/booking', methods=['POST', 'OPTIONS'])  # Явно разрешаем POST и OPTIONS
def create_booking():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    try:
        data = request.get_json()

        required = ['roomId', 'bookingDates', 'firstName', 'lastName']
        if not all(field in data for field in required):
            return jsonify({"error": "Missing required fields"}), 400

        room_id = data['roomId']
        check_in = data['bookingDates']['checkIn']
        check_out = data['bookingDates']['checkOut']

        if not any(room['roomId'] == room_id for room in rooms):
            return jsonify({"error": "Room not found"}), 404

        if not is_room_available(room_id, check_in, check_out):
            return jsonify({"error": "Room already booked"}), 409

        booking_id = len(bookings) + 1
        bookings.append(
            {
                'bookingId': booking_id,
                'roomId': room_id,
                'firstName': data['firstName'],
                'lastName': data['lastName'],
                'bookingDates': {'checkIn': check_in, 'checkOut': check_out},
            }
        )

        return jsonify({"message": "Booking created", "bookingId": booking_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
