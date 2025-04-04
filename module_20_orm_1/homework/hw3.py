from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    @classmethod
    def get_students_with_scholarship(cls, session):
        """
        Возвращает список студентов, которые получают стипендию

        :param session: SQLAlchemy session
        :return: List[Student] - список студентов со стипендией
        """
        return session.query(cls).filter(cls.scholarship == True).all()

    @classmethod
    def get_students_above_score(cls, session, min_score):
        """
        Возвращает список студентов, у которых средний балл выше заданного

        :param session: SQLAlchemy session
        :param min_score: минимальный средний балл для фильтрации
        :return: List[Student] - список студентов с баллом выше min_score
        """
        return session.query(cls).filter(cls.average_score > min_score).all()