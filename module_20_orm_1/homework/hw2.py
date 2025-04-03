from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

Base = declarative_base()


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    @hybrid_property
    def count_date_with_book(self):
        """Количество дней, которые книга была у студента"""
        return_date = self.date_of_return if self.date_of_return else datetime.now()
        delta = return_date - self.date_of_issue
        return delta.days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        """SQL-выражение для вычисления количества дней"""
        return func.coalesce(
            func.julianday(func.ifnull(cls.date_of_return, datetime.now())) -
            func.julianday(cls.date_of_issue)
        )