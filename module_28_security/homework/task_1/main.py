from flask import Flask, jsonify, request, Response

app = Flask(__name__)

ALLOWED_ORIGIN = 'https://google.com'

@app.route('/', methods=['GET'])
def get_handler():
    print(request.headers)
    return jsonify({'message': 'GET request processed'})

@app.route('/', methods=['POST'])
def post_handler():
    print(request.headers)
    return jsonify({'message': 'POST request processed'})

@app.after_request
def add_cors(response: Response):
    # Проверяем, есть ли Origin в заголовках и совпадает ли он с разрешенным
    origin = request.headers.get('Origin')
    if origin and origin == ALLOWED_ORIGIN:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        response.headers['Access-Control-Allow-Headers'] = 'X-My-Fancy-Header'
    return response

if __name__ == '__main__':
    app.run(port=8080, debug=True)