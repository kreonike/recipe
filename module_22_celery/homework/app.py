import uuid

from celery.result import AsyncResult
from flask import Flask, request, jsonify

from config import celery_app
from config import subscribed_emails

app = Flask(__name__)


@app.route('/blur', methods=['POST'])
def blur_images():
    if 'images' not in request.files:
        return jsonify({"error": "No images provided"}), 400

    email = request.form.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    images = request.files.getlist('images')
    if not images:
        return jsonify({"error": "No images provided"}), 400

    order_id = str(uuid.uuid4())
    tasks = []

    # Save images temporarily and create tasks
    for img in images:
        filename = f"temp_{order_id}_{img.filename}"
        img.save(filename)
        task = celery_app.send_task(
            'celery_worker.process_image', args=[filename, order_id, email]
        )
        tasks.append(task)

    return (
        jsonify(
            {
                "order_id": order_id,
                "task_count": len(tasks),
                "task_ids": [task.id for task in tasks],
            }
        ),
        202,
    )


@app.route('/status/<task_id>')
def get_status(task_id):
    task = AsyncResult(task_id)

    if task.ready():
        return jsonify({"status": "completed", "result": task.result})
    else:
        return jsonify({"status": "processing"})


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    subscribed_emails.add(email)
    return jsonify({"message": "Subscribed successfully"}), 200


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    if email in subscribed_emails:
        subscribed_emails.remove(email)
    return jsonify({"message": "Unsubscribed successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
