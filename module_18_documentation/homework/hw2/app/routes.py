import os
import sqlite3

from flask import Flask, request
from flask_restx import Api, Resource, fields
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError

from werkzeug.serving import WSGIRequestHandler
WSGIRequestHandler.protocol_version = "HTTP/1.1"

from models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
    DATABASE_NAME,
    BOOKS_TABLE_NAME,
    AUTHORS_TABLE_NAME,
    _get_book_obj_from_row,
    get_author_with_books,
    delete_author,
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Books API',
    description='A simple Books and Authors management API',
    doc='/api/docs',
)

books_ns = api.namespace('api/books', description='Books operations')
authors_ns = api.namespace('api/authors', description='Authors operations')

author_model = api.model(
    'Author',
    {
        'id': fields.Integer(readOnly=True, description='The author unique identifier'),
        'first_name': fields.String(required=True, description='First name'),
        'last_name': fields.String(required=True, description='Last name'),
        'middle_name': fields.String(description='Middle name (optional)'),
    },
)

book_model = api.model(
    'Book',
    {
        'id': fields.Integer(readOnly=True, description='The book unique identifier'),
        'title': fields.String(required=True, description='Book title'),
        'author_id': fields.Integer(required=True, description='Author ID'),
    },
)


@api.errorhandler(NotFound)
def handle_not_found(error):
    return {'message': 'Resource not found'}, 404


@api.errorhandler(BadRequest)
def handle_bad_request(error):
    return {'message': 'Bad request'}, 400


@api.errorhandler(InternalServerError)
def handle_server_error(error):
    return {'message': 'Internal server error'}, 500


@books_ns.route('/')
class BookList(Resource):
    @books_ns.doc('list_books')
    @books_ns.marshal_list_with(book_model)
    def get(self):
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True)

    @books_ns.doc('create_book')
    @books_ns.expect(book_model)
    @books_ns.marshal_with(book_model, code=201)
    def post(self):
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
            book = add_book(book)
            return schema.dump(book), 201
        except ValidationError as exc:
            api.abort(400, 'Validation error', errors=exc.messages)


@books_ns.route('/<int:book_id>')
@books_ns.response(404, 'Book not found')
@books_ns.param('book_id', 'The book identifier')
class BookResource(Resource):
    @books_ns.doc('get_book')
    @books_ns.marshal_with(book_model)
    def get(self, book_id):
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f'SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?', (book_id,)
            )
            book = cursor.fetchone()

        if not book:
            api.abort(404, message='Book not found')

        return _get_book_obj_from_row(book)

    @books_ns.doc('update_book')
    @books_ns.expect(book_model)
    @books_ns.marshal_with(book_model)
    def put(self, book_id):
        data = request.json
        schema = BookSchema()

        try:
            with sqlite3.connect(DATABASE_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f'SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?', (book_id,)
                )
                if not cursor.fetchone():
                    api.abort(404, message='Book not found')

            book_data = schema.load(data)

            with sqlite3.connect(DATABASE_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"""
                    UPDATE `{BOOKS_TABLE_NAME}`
                    SET title = ?, author_id = ?
                    WHERE id = ?
                    """,
                    (book_data.title, book_data.author_id, book_id),
                )
                conn.commit()

            return self.get(book_id)

        except ValidationError as exc:
            api.abort(400, 'Validation error', errors=exc.messages)

    @books_ns.doc('patch_book')
    @books_ns.expect(book_model)
    @books_ns.marshal_with(book_model)
    def patch(self, book_id):
        data = request.json
        schema = BookSchema(partial=True)

        try:
            with sqlite3.connect(DATABASE_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f'SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?', (book_id,)
                )
                book = cursor.fetchone()

            if not book:
                api.abort(404, message='Book not found')

            current_book = _get_book_obj_from_row(book)
            current_data = BookSchema().dump(current_book)

            updated_data = {**current_data, **data}

            book_data = schema.load(updated_data)

            with sqlite3.connect(DATABASE_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"""
                    UPDATE `{BOOKS_TABLE_NAME}`
                    SET title = ?, author_id = ?
                    WHERE id = ?
                    """,
                    (book_data.title, book_data.author_id, book_id),
                )
                conn.commit()

            return self.get(book_id)

        except ValidationError as exc:
            api.abort(400, 'Validation error', errors=exc.messages)

    @books_ns.doc('delete_book')
    @books_ns.response(204, 'Book deleted')
    def delete(self, book_id):
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute(
                f'SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?', (book_id,)
            )
            if not cursor.fetchone():
                api.abort(404, message="Book not found")

            cursor.execute(f'DELETE FROM `{BOOKS_TABLE_NAME}` WHERE id = ?', (book_id,))
            conn.commit()

        return '', 204


@authors_ns.route('/')
class AuthorList(Resource):
    @authors_ns.doc('create_author')
    @authors_ns.expect(author_model)
    @authors_ns.marshal_with(author_model, code=201)
    def post(self):
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)

            with sqlite3.connect(DATABASE_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"""
                    INSERT INTO `{AUTHORS_TABLE_NAME}`
                    (first_name, last_name, middle_name) VALUES (?, ?, ?)
                    """,
                    (author.first_name, author.last_name, author.middle_name),
                )
                author.id = cursor.lastrowid
                conn.commit()

            return schema.dump(author), 201
        except ValidationError as exc:
            api.abort(400, 'Validation error', errors=exc.messages)
        except sqlite3.Error as e:
            api.abort(500, 'Database error', error=str(e))


@authors_ns.route('/<int:author_id>')
@authors_ns.response(404, 'Author not found')
@authors_ns.param('author_id', 'The author identifier')
class AuthorResource(Resource):
    @authors_ns.doc('get_author')
    @authors_ns.marshal_with(author_model)
    def get(self, author_id):
        author_data = get_author_with_books(author_id)
        if not author_data:
            api.abort(404, message='Author not found')
        return author_data

    @authors_ns.doc('delete_author')
    @authors_ns.response(204, 'Author deleted')
    def delete(self, author_id):
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f'SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?', (author_id,)
            )
            if not cursor.fetchone():
                api.abort(404, message="Author not found")

            delete_author(author_id)

        return '', 204


if __name__ == '__main__':
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
    init_db(initial_records=DATA)
    app.run(debug=True)
