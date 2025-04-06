from flask import Flask, request, jsonify
from sqlalchemy import create_engine, func, case, and_, or_
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models import Base, Book, Student, ReceivingBook

app = Flask(__name__)

engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@app.route('/books', methods=['GET'])
def get_all_books():
    """Получить все книги в библиотеке"""
    session = Session()
    try:
        books = session.query(Book).all()
        return jsonify([{
            'id': book.id,
            'name': book.name,
            'count': book.count,
            'release_date': book.release_date.isoformat(),
            'author_id': book.author_id
        } for book in books]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/debtors', methods=['GET'])
def get_debtors():
    """Получить список должников (держали книги более 14 дней, включая уже возвращенные)"""
    session = Session()
    try:
        debtors = session.query(Student, Book, ReceivingBook) \
            .join(ReceivingBook, ReceivingBook.student_id == Student.id) \
            .join(Book, ReceivingBook.book_id == Book.id) \
            .filter(
                or_(
                    and_(
                        ReceivingBook.date_of_return == None,
                        ReceivingBook.date_of_issue < datetime.now() - timedelta(days=14)
                    ),
                    and_(
                        ReceivingBook.date_of_return != None,
                        ReceivingBook.date_of_return - ReceivingBook.date_of_issue > timedelta(days=14)
                    )
                )
            ).all()

        result = [{
            'student_id': student.id,
            'student_name': f"{student.name} {student.surname}",
            'book_id': book.id,
            'book_name': book.name,
            'days_with_book': (datetime.now() - receiving.date_of_issue).days if receiving.date_of_return is None
                              else (receiving.date_of_return - receiving.date_of_issue).days,
            'is_returned': receiving.date_of_return is not None
        } for student, book, receiving in debtors]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/issue-book', methods=['POST'])
def issue_book():
    """Выдать книгу студенту"""
    session = Session()
    try:
        data = request.get_json()
        book_id = data.get('book_id')
        student_id = data.get('student_id')

        if not book_id or not student_id:
            return jsonify({'error': 'Missing book_id or student_id'}), 400

        book = session.query(Book).get(book_id)
        student = session.query(Student).get(student_id)

        if not book:
            return jsonify({'error': 'Book not found'}), 404
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        new_issue = ReceivingBook(
            book_id=book_id,
            student_id=student_id,
            date_of_issue=datetime.now(),
            date_of_return=None
        )

        session.add(new_issue)
        session.commit()

        return jsonify({
            'message': 'Book issued successfully',
            'issue_id': new_issue.id
        }), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/return-book', methods=['POST'])
def return_book():
    """Сдать книгу в библиотеку"""
    session = Session()
    try:
        data = request.get_json()
        book_id = data.get('book_id')
        student_id = data.get('student_id')

        if not book_id or not student_id:
            return jsonify({'error': 'Missing book_id or student_id'}), 400

        issue = session.query(ReceivingBook) \
            .filter(
            ReceivingBook.book_id == book_id,
            ReceivingBook.student_id == student_id,
            ReceivingBook.date_of_return == None
        ).first()

        if not issue:
            return jsonify({'error': 'Active book issue not found'}), 404

        issue.date_of_return = datetime.now()
        session.commit()

        return jsonify({
            'message': 'Book returned successfully',
            'days_kept': (issue.date_of_return - issue.date_of_issue).days
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/books/available-by-author/<int:author_id>', methods=['GET'])
def get_available_books_by_author(author_id):
    """Получить количество оставшихся в библиотеке книг по автору"""
    session = Session()
    try:
        available_books = session.query(
            Book.name,
            Book.count,
            func.coalesce(
                func.sum(
                    case(
                        (ReceivingBook.date_of_return == None, 1),
                        else_=0
                    )
                ), 0
            ).label('borrowed'),
            (Book.count - func.coalesce(
                func.sum(
                    case(
                        (ReceivingBook.date_of_return == None, 1),
                        else_=0
                    )
                ), 0
            )).label('available')
        ).outerjoin(
            ReceivingBook, ReceivingBook.book_id == Book.id
        ).filter(
            Book.author_id == author_id
        ).group_by(
            Book.id
        ).all()

        if not available_books:
            return jsonify({'error': 'Author not found or no books available'}), 404

        result = [{
            'book_name': book.name,
            'total_count': book.count,
            'borrowed_count': book.borrowed,
            'available_count': book.available
        } for book in available_books]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/students/<int:student_id>/unread-books', methods=['GET'])
def get_unread_books_by_authors(student_id):
    """Получить список книг, которые студент не читал, но читал других авторов"""
    session = Session()
    try:
        read_authors = session.query(
            Book.author_id
        ).join(
            ReceivingBook, ReceivingBook.book_id == Book.id
        ).filter(
            ReceivingBook.student_id == student_id
        ).distinct().subquery()

        unread_books = session.query(Book).join(
            read_authors, read_authors.c.author_id == Book.author_id
        ).outerjoin(
            ReceivingBook, and_(
                ReceivingBook.book_id == Book.id,
                ReceivingBook.student_id == student_id
            )
        ).filter(
            ReceivingBook.id == None
        ).all()

        result = [{
            'book_id': book.id,
            'book_name': book.name,
            'author_id': book.author_id
        } for book in unread_books]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/stats/avg-books-this-month', methods=['GET'])
def get_avg_books_this_month():
    """Получить среднее количество книг, которые студенты брали в этом месяце"""
    session = Session()
    try:
        current_month = datetime.now().month
        current_year = datetime.now().year

        books_per_student = session.query(
            ReceivingBook.student_id,
            func.count(ReceivingBook.id).label('book_count')
        ).filter(
            func.extract('month', ReceivingBook.date_of_issue) == current_month,
            func.extract('year', ReceivingBook.date_of_issue) == current_year
        ).group_by(
            ReceivingBook.student_id
        ).subquery()

        avg_books = session.query(
            func.avg(books_per_student.c.book_count).label('avg_books')
        ).scalar()

        return jsonify({
            'month': current_month,
            'year': current_year,
            'avg_books': float(avg_books) if avg_books else 0
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/stats/top-book-high-score', methods=['GET'])
def get_top_book_high_score():
    """Получить самую популярную книгу среди студентов с средним баллом > 4.0"""
    session = Session()
    try:
        top_book = session.query(
            Book.id,
            Book.name,
            func.count(ReceivingBook.id).label('borrow_count')
        ).join(
            ReceivingBook, ReceivingBook.book_id == Book.id
        ).join(
            Student, Student.id == ReceivingBook.student_id
        ).filter(
            Student.average_score > 4.0
        ).group_by(
            Book.id
        ).order_by(
            func.count(ReceivingBook.id).desc()
        ).first()

        if not top_book:
            return jsonify({'message': 'No books found for students with score > 4.0'}), 404

        return jsonify({
            'book_id': top_book.id,
            'book_name': top_book.name,
            'borrow_count': top_book.borrow_count
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/stats/top-readers-this-year', methods=['GET'])
def get_top_readers_this_year():
    """Получить ТОП-10 самых читающих студентов в этом году"""
    session = Session()
    try:
        current_year = datetime.now().year

        top_students = session.query(
            Student.id,
            Student.name,
            Student.surname,
            func.count(ReceivingBook.id).label('books_read')
        ).join(
            ReceivingBook, ReceivingBook.student_id == Student.id
        ).filter(
            func.extract('year', ReceivingBook.date_of_issue) == current_year
        ).group_by(
            Student.id
        ).order_by(
            func.count(ReceivingBook.id).desc()
        ).limit(10).all()

        result = [{
            'student_id': student.id,
            'student_name': f"{student.name} {student.surname}",
            'books_read': student.books_read
        } for student in top_students]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug=True)