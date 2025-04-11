from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import logging

app = Flask(__name__)
metrics = PrometheusMetrics(app)

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

@app.route('/hello')
@metrics.counter(
    'hello_endpoint_counter',
    'Count of requests to /hello endpoint',
    labels={'status': lambda resp: resp.status_code}
)
def hello():
    app.logger.debug("Processing /hello request")
    return jsonify({'message': 'Hello, World!'})

@app.route('/example')
@metrics.counter(
    'example_endpoint_counter',
    'Count of requests to /example endpoint',
    labels={'status': lambda resp: resp.status_code}
)
def example():
    app.logger.debug("Processing /example request")
    return jsonify({'result': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)