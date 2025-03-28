from flask import Flask, render_template, request, redirect, url_for, abort

from forms import BookForm
from models import (
    init_db,
    get_all_books,
    get_books_by_author,
    add_book,
    increment_views,
    get_book_by_id,
    DATA,
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'


@app.route('/books')
def all_books():
    books = get_all_books()
    total_books = len(books)
    return render_template(
        'index.html',
        books=books,
        total_books=total_books,
        page_title=f'Total books in library: {total_books}',
    )


@app.route('/books/<int:book_id>')
def book_details(book_id):
    book = get_book_by_id(book_id)
    if not book:
        abort(404)

    increment_views(book_id)
    book = get_book_by_id(book_id)
    return render_template(
        'book_details.html', book=book, page_title=f'Book: {book.title}'
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
