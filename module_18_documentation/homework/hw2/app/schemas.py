import sqlite3

from marshmallow import Schema, fields, validates, ValidationError, post_load

from models import (
    get_book_by_title,
    Book,
    Author,
    get_author_by_id,
    DATABASE_NAME,
    AUTHORS_TABLE_NAME,
)


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(required=False, allow_none=True)

    @post_load
    def create_author(self, data: dict) -> Author:
        return Author(**data)


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Int(required=False)
    author = fields.Nested(AuthorSchema, required=False)

    @validates('title')
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                'please use a different title.'.format(title=title)
            )

    @validates('author_id')
    def validate_author_id(self, author_id: int) -> None:
        if author_id is not None and get_author_by_id(author_id) is None:
            raise ValidationError('Author with this ID does not exist.')

    @post_load
    def create_book(self, data: dict) -> Book:
        author_data = data.pop('author', None)
        if author_data:
            author = AuthorSchema().load(author_data)
            with sqlite3.connect(DATABASE_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"""
                    INSERT INTO `{AUTHORS_TABLE_NAME}`
                    (first_name, last_name, middle_name) VALUES (?, ?, ?)
                    """,
                    (author.first_name, author.last_name, author.middle_name),
                )
                data['author_id'] = cursor.lastrowid
                conn.commit()
        return Book(**data)
