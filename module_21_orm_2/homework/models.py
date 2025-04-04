from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete='CASCADE'), nullable=False)

    author = relationship("Author", back_populates="books")
    receiving_books = relationship(
        "ReceivingBook",
        back_populates="book",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    students = association_proxy('receiving_books', 'student',
                                 creator=lambda student: ReceivingBook(student=student))


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    books = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete",
        passive_deletes=True,
        lazy='joined'
    )


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    receiving_books = relationship(
        "ReceivingBook",
        back_populates="student",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy='dynamic'
    )

    books = association_proxy('receiving_books', 'book',
                              creator=lambda book: ReceivingBook(book=book))


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)


    book = relationship(
        "Book",
        back_populates="receiving_books",
        lazy='joined'
    )
    student = relationship(
        "Student",
        back_populates="receiving_books",
        lazy='joined'
    )