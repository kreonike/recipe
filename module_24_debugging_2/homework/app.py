from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@metrics.counter(
    'hello_endpoint_counter',
    'Count of requests to /hello endpoint',
    labels={'status': lambda r: r.status_code}
)

@app.route('/hello')
def hello():
    return jsonify({'message': 'Hello, World!'})

@metrics.counter(
    'example_endpoint_counter',
    'Count of requests to /example endpoint',
    labels={'status': lambda r: r.status_code}
)
@app.route('/example')
def example():
    return jsonify({'result': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)