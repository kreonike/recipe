import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Список для хранения логов
logs_storage = []


@app.route("/log", methods=["POST"])
def log():
    """
    Записываем полученные логи, которые пришли к нам на сервер.
    :return: текстовое сообщение об успешной записи, статус код успешной работы
    """
    try:
        # Получаем JSON-данные из запроса
        log_data = request.get_json()  # Используем get_json() для получения JSON
        if log_data:
            # Добавляем лог в хранилище
            logs_storage.append(log_data)
            print(f"Log received: {log_data}")  # Отладочное сообщение
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Log received and stored successfully.",
                    }
                ),
                200,
            )
        else:
            print("No log data provided.")  # Отладочное сообщение
            return jsonify({"status": "error", "message": "No log data provided."}), 400
    except Exception as e:
        print(f"Error processing log: {str(e)}")  # Отладочное сообщение
        return (
            jsonify({"status": "error", "message": f"Error processing log: {str(e)}"}),
            500,
        )


@app.route("/logs", methods=["GET"])
def logs():
    """
    Рендерим список полученных логов.
    :return: список логов, обернутый в тег HTML <pre></pre>
    """
    # Преобразуем логи в строку для отображения
    logs_str = json.dumps(logs_storage, indent=4)
    print(f"Logs requested: {logs_str}")  # Отладочное сообщение
    return f"<pre>{logs_str}</pre>"


if __name__ == "__main__":
    # Запускаем сервер на localhost:3000
    print("Starting server on http://127.0.0.1:3000")
    app.run(host="127.0.0.1", port=3000)
