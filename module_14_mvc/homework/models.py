import sqlite3
from typing import Any, Optional, List, Dict

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.', 'views': 0},
    {
        'id': 1,
        'title': 'Moby-Dick; or, The Whale',
        'author': 'Herman Melville',
        'views': 0,
    },
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy', 'views': 0},
]


class Book:
    def __init__(self, id: int, title: str, author: str, views: int = 0) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.views: int = views

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[Dict[str, Any]]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS `table_books` (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                views INTEGER DEFAULT 0 NOT NULL
            )
            """
        )
        # Проверяем, есть ли уже данные в таблице
        cursor.execute("SELECT COUNT(*) FROM table_books")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO `table_books` (title, author, views) VALUES (?, ?, ?)",
                [
                    (item['title'], item['author'], item.get('views', 0))
                    for item in initial_records
                ],
            )
        conn.commit()


def increment_views(book_id: int) -> Book:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "UPDATE table_books SET views = views + 1 WHERE id = ? RETURNING *",
            (book_id,),
        )
        result = cursor.fetchone()
        conn.commit()
        if result:
            return Book(*result)
        return None


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT * FROM table_books WHERE id = ?", (book_id,))
        result = cursor.fetchone()
        if result:
            return Book(*result)
        return None


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT * FROM `table_books`")
        return [Book(*row) for row in cursor.fetchall()]


def get_books_by_author(author: str) -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM `table_books` WHERE author LIKE ?", (f'%{author}%',)
        )
        return [Book(*row) for row in cursor.fetchall()]


def get_total_books_count() -> int:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM `table_books`")
        return cursor.fetchone()[0]


def add_book(title: str, author: str) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO `table_books` (title, author) VALUES (?, ?)", (title, author)
        )
        conn.commit()
