"""
Contains the database classes for the application
"""


from sqlalchemy import Column, Boolean, String, Integer
from database import Base


class SectionOneQnA(Base):
    __tablename__ = 'SectionOneQnA'

    question = Column(String, primary_key=True)
    answer = Column(String, primary_key=True)
    is_correct = Column(Boolean, nullable=False)


class SectionTwoAndThreeQuestions(Base):
    __tablename__ = 'SectionTwoAndThreeQuestions'

    question = Column(String, primary_key=True)
    section = Column(Integer, nullable=False)

