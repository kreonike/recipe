"""
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное.
Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить
список всех доступных страниц на сайте с возможностью перехода на них.
"""

from flask import Flask, render_template_string

app = Flask(__name__)


@app.route('/dogs')
def dogs():
    return 'Страница с пёсиками'


@app.route('/cats')
def cats():
    return 'Страница с котиками'


@app.route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'


@app.route('/index')
def index():
    return 'Главная страница'


@app.errorhandler(404)
def page_not_found(error):
    links = []
    for rule in app.url_map.iter_rules():
        if 'static' not in rule.endpoint and '<' not in rule.rule:
            links.append(f'<a href="{rule.rule}">{rule.rule}</a>')

    html = """
    <h1>Страница не найдена</h1>
    <p>Возможно, вы искали одну из следующих страниц:</p>
    <ul>
        {% for link in links %}
        <li>{{ link | safe }}</li>
        {% endfor %}
    </ul>
    """
    return render_template_string(html, links=links), 404


if __name__ == '__main__':
    app.run(debug=True)