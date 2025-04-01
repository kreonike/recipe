import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {
        'id': 0,
        'title': 'A Byte of Python',
        'author': {'first_name': 'Swaroop', 'last_name': 'C. H.', 'middle_name': None},
    },
    {
        'id': 1,
        'title': 'Moby-Dick; or, The Whale',
        'author': {
            'first_name': 'Herman',
            'last_name': 'Melville',
            'middle_name': None,
        },
    },
    {
        'id': 3,
        'title': 'War and Peace',
        'author': {'first_name': 'Leo', 'last_name': 'Tolstoy', 'middle_name': None},
    },
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"


@dataclass
class Book:
    title: str
    author_id: int
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS `{AUTHORS_TABLE_NAME}`(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                middle_name TEXT
            );
            """
        )

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS `{BOOKS_TABLE_NAME}`(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                FOREIGN KEY (author_id) REFERENCES {AUTHORS_TABLE_NAME}(id) ON DELETE CASCADE
            );
            """
        )

        for item in initial_records:
            author_data = item['author']
            cursor.execute(
                f"""
                INSERT INTO `{AUTHORS_TABLE_NAME}`
                (first_name, last_name, middle_name) VALUES (?, ?, ?)
                """,
                (
                    author_data['first_name'],
                    author_data['last_name'],
                    author_data['middle_name'],
                ),
            )
            author_id = cursor.lastrowid
            cursor.execute(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author_id) VALUES (?, ?)
                """,
                (item['title'], author_id),
            )

        conn.commit()


def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author_id=row[2])


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?
            """,
            (author_id,),
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}`
            (title, author_id) VALUES (?, ?)
            """,
            (book.title, book.author_id),
        )
        book.id = cursor.lastrowid
        return book


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,),
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_author_with_books(author_id: int) -> Optional[Dict]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT a.*, b.id as book_id, b.title as book_title
            FROM `{AUTHORS_TABLE_NAME}` a
            LEFT JOIN `{BOOKS_TABLE_NAME}` b ON a.id = b.author_id
            WHERE a.id = ?
            """,
            (author_id,),
        )
        rows = cursor.fetchall()
        if not rows:
            return None

        author_data = {
            'id': rows[0][0],
            'first_name': rows[0][1],
            'last_name': rows[0][2],
            'middle_name': rows[0][3],
            'books': [],
        }

        for row in rows:
            if row[4]:
                author_data['books'].append({'id': row[4], 'title': row[5]})

        return author_data


def delete_author(author_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'DELETE FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?',
            (author_id,),
        )
        conn.commit()
