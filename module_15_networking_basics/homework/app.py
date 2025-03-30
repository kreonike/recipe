from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/rooms/*": {"origins": "*"}, r"/bookings/*": {"origins": "*"}})

# In-memory data storage
rooms = []
bookings = []


def is_room_available(room_id, check_in, check_out):
    """Check if room is available for given dates"""
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


@app.route('/rooms', methods=['GET', 'POST'])
def handle_rooms():
    """Handle both creation and listing of rooms"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            required_fields = ['floor', 'beds', 'guestNum', 'price']
            if not all(field in data for field in required_fields):
                return (
                    jsonify(
                        {
                            "error": "Missing required fields",
                            "_links": {"documentation": {"href": "/docs#create-room"}},
                        }
                    ),
                    400,
                )

            room_id = max(room['roomId'] for room in rooms) + 1 if rooms else 1
            new_room = {
                'roomId': room_id,
                'floor': data['floor'],
                'beds': data['beds'],
                'guestNum': data['guestNum'],
                'price': data['price'],
                '_links': {
                    'self': {'href': f'/rooms/{room_id}'},
                    'bookings': {'href': '/bookings', 'method': 'POST'},
                    'availability': {'href': f'/rooms/{room_id}/availability'},
                },
            }

            rooms.append(new_room)
            return jsonify(new_room), 201, {'Location': f'/rooms/{room_id}'}
        except Exception as e:
            return (
                jsonify(
                    {
                        "error": str(e),
                        "_links": {
                            "retry": {"href": "/rooms", "method": "POST"},
                            "documentation": {"href": "/docs#errors"},
                        },
                    }
                ),
                500,
            )
    else:
        try:
            check_in = request.args.get('checkIn', '20210101')
            check_out = request.args.get('checkOut', '20211231')
            guests_num = int(request.args.get('guestsNum', 1))

            available_rooms = [
                {
                    **room,
                    '_links': {
                        'self': {'href': f'/rooms/{room["roomId"]}'},
                        'book': {'href': '/bookings', 'method': 'POST'},
                    },
                }
                for room in rooms
                if (
                    room['guestNum'] >= guests_num
                    and is_room_available(room['roomId'], check_in, check_out)
                )
            ]

            response = {
                'count': len(available_rooms),
                'rooms': available_rooms,
                '_links': {
                    'self': {'href': request.url},
                    'create': {'href': '/rooms', 'method': 'POST'},
                    'documentation': {'href': '/docs#list-rooms'},
                },
            }
            return jsonify(response), 200
        except Exception as e:
            return (
                jsonify(
                    {
                        "error": str(e),
                        "_links": {"documentation": {"href": "/docs#errors"}},
                    }
                ),
                500,
            )


@app.route('/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    """Get specific room details"""
    try:
        room = next((r for r in rooms if r['roomId'] == room_id), None)
        if not room:
            return (
                jsonify(
                    {
                        "error": "Room not found",
                        "_links": {
                            "list": {"href": "/rooms"},
                            "documentation": {"href": "/docs#get-room"},
                        },
                    }
                ),
                404,
            )

        response = {
            **room,
            '_links': {
                'self': {'href': f'/rooms/{room_id}'},
                'bookings': {'href': '/bookings', 'method': 'POST'},
                'availability': {'href': f'/rooms/{room_id}/availability'},
            },
        }
        return jsonify(response), 200
    except Exception as e:
        return (
            jsonify(
                {"error": str(e), "_links": {"documentation": {"href": "/docs#errors"}}}
            ),
            500,
        )


@app.route('/rooms/<int:room_id>/availability', methods=['GET'])
def check_availability(room_id):
    """Check room availability for given dates"""
    try:
        check_in = request.args.get('checkIn', '20210101')
        check_out = request.args.get('checkOut', '20211231')

        room = next((r for r in rooms if r['roomId'] == room_id), None)
        if not room:
            return (
                jsonify(
                    {
                        "error": "Room not found",
                        "_links": {
                            "list": {"href": "/rooms"},
                            "documentation": {"href": "/docs#availability"},
                        },
                    }
                ),
                404,
            )

        is_available = is_room_available(room_id, check_in, check_out)

        response = {
            "roomId": room_id,
            "checkIn": check_in,
            "checkOut": check_out,
            "isAvailable": is_available,
            '_links': {
                'self': {
                    'href': f'/rooms/{room_id}/availability?checkIn={check_in}&checkOut={check_out}'
                },
                'room': {'href': f'/rooms/{room_id}'},
                'book': {'href': '/bookings', 'method': 'POST'},
            },
        }
        return jsonify(response), 200
    except Exception as e:
        return (
            jsonify(
                {"error": str(e), "_links": {"documentation": {"href": "/docs#errors"}}}
            ),
            500,
        )


@app.route('/bookings', methods=['POST'])
def create_booking():
    """Create a new booking"""
    try:
        data = request.get_json()
        required = ['roomId', 'bookingDates', 'firstName', 'lastName']
        if not all(field in data for field in required):
            return (
                jsonify(
                    {
                        "error": "Missing required fields",
                        "_links": {"documentation": {"href": "/docs#create-booking"}},
                    }
                ),
                400,
            )

        room_id = data['roomId']
        check_in = data['bookingDates']['checkIn']
        check_out = data['bookingDates']['checkOut']

        room = next((r for r in rooms if r['roomId'] == room_id), None)
        if not room:
            return (
                jsonify(
                    {
                        "error": "Room not found",
                        "_links": {
                            "list": {"href": "/rooms"},
                            "documentation": {"href": "/docs#create-booking"},
                        },
                    }
                ),
                404,
            )

        if not is_room_available(room_id, check_in, check_out):
            return (
                jsonify(
                    {
                        "error": "Room already booked for these dates",
                        "_links": {
                            "room": {"href": f'/rooms/{room_id}'},
                            "availability": {"href": f'/rooms/{room_id}/availability'},
                        },
                    }
                ),
                409,
            )

        booking_id = len(bookings) + 1
        new_booking = {
            'bookingId': booking_id,
            'roomId': room_id,
            'firstName': data['firstName'],
            'lastName': data['lastName'],
            'bookingDates': {'checkIn': check_in, 'checkOut': check_out},
            'status': 'confirmed',
            '_links': {
                'self': {'href': f'/bookings/{booking_id}'},
                'room': {'href': f'/rooms/{room_id}'},
                'payment': {'href': '/payments', 'method': 'POST'},
                'cancel': {'href': f'/bookings/{booking_id}', 'method': 'DELETE'},
            },
        }

        bookings.append(new_booking)
        return jsonify(new_booking), 201, {'Location': f'/bookings/{booking_id}'}
    except Exception as e:
        return (
            jsonify(
                {"error": str(e), "_links": {"documentation": {"href": "/docs#errors"}}}
            ),
            500,
        )


@app.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Get booking details"""
    try:
        booking = next((b for b in bookings if b['bookingId'] == booking_id), None)
        if not booking:
            return (
                jsonify(
                    {
                        "error": "Booking not found",
                        "_links": {
                            "create": {"href": "/bookings", "method": "POST"},
                            "documentation": {"href": "/docs#get-booking"},
                        },
                    }
                ),
                404,
            )

        return jsonify(booking), 200
    except Exception as e:
        return (
            jsonify(
                {"error": str(e), "_links": {"documentation": {"href": "/docs#errors"}}}
            ),
            500,
        )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
