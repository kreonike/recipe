from flask import Flask, request, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models import Base, Book, Student, ReceivingBook  # Предполагаем, что модели определены в отдельном файле

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
    """Получить список должников (держат книги более 14 дней)"""
    session = Session()
    try:
        fourteen_days_ago = datetime.now() - timedelta(days=14)

        debtors = session.query(Student, Book, ReceivingBook) \
            .join(ReceivingBook, ReceivingBook.student_id == Student.id) \
            .join(Book, ReceivingBook.book_id == Book.id) \
            .filter(
            ReceivingBook.date_of_return == None,
            ReceivingBook.date_of_issue < fourteen_days_ago
        ).all()

        result = [{
            'student_id': student.id,
            'student_name': f"{student.name} {student.surname}",
            'book_id': book.id,
            'book_name': book.name,
            'days_with_book': (datetime.now() - receiving.date_of_issue).days
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


if __name__ == '__main__':
    app.run(debug=True)