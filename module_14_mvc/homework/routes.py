from flask import Flask, render_template, request, redirect, url_for

from forms import BookForm
from models import (
    init_db,
    get_all_books,
    get_books_by_author,
    add_book,
    increment_views,
    DATA,
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'


@app.route('/books')
def all_books():
    books = get_all_books()
    # Инкрементируем просмотры для каждой книги
    for book in books:
        increment_views(book.id)
    total_books = len(books)
    return render_template(
        'index.html',
        books=books,
        total_books=total_books,
        page_title=f'Total books in library: {total_books}',
    )


@app.route('/books/search', methods=['GET'])
def book_search():
    author_name = request.args.get('author', '').strip()
    books = get_books_by_author(author_name)
    # Инкрементируем просмотры для каждой найденной книги
    for book in books:
        increment_views(book.id)
    return render_template(
        'search_results.html',
        books=books,
        author_name=author_name,
        page_title=f'Search results for: {author_name}',
    )


@app.route('/books/search', methods=['GET'])
def book_search():
    author_name = request.args.get('author', '').strip()
    books = get_books_by_author(author_name)
    return render_template(
        'search_results.html',
        books=books,
        author_name=author_name,
        page_title=f'Search results for: {author_name}',
    )


@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form():
    form = BookForm()
    if form.validate_on_submit():
        add_book(form.title.data, form.author.data)
        return redirect(url_for('all_books'))
    return render_template('add_book.html', form=form)


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
