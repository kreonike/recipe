from flask import Flask, request, Response

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {user_input}
</body>
</html>
"""


@app.route('/', methods=['GET'])
def handler():
    user_input = request.args.get('input', '')
    rendered_html = HTML.format(user_input=user_input)

    response = Response(rendered_html)

    response.headers['Content-Security-Policy'] = "script-src 'self'"

    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)