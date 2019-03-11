"""
Contains the database classes for the application
"""


from sqlalchemy import Column, Boolean, String, Integer, Date, ForeignKeyConstraint
from database import Base


class StudentTeam(Base):
    __tablename__ = 'StudentTeams'

    name = Column(String, primary_key=True)
    year = Column(Date, primary_key=True)
    first_student = Column(String, nullable=False)
    second_student = Column(String)
    password = Column(String, nullable=False)


class StudentAnswer(Base):
    __tablename__ = 'StudentAnswers'

    team_name = Column(String, primary_key=True)
    team_year = Column(Date, primary_key=True)
    section = Column(Integer, nullable=False)
    question = Column(String, primary_key=True)
    answer = Column(String)

    __table_args__ = (
        ForeignKeyConstraint(['team_name', 'team_year'], ['StudentTeams.name', 'StudentTeams.year']),
    )


#class SectionOneQnA(Base):
#    __tablename__ = 'SectionOneQnAs'
#
#    question = Column(String, primary_key=True)
#    answer = Column(String, primary_key=True)
#    is_correct = Column(Boolean, nullable=False)


#class SectionTwoAndThreeQuestion(Base):
#    __tablename__ = 'SectionTwoAndThreeQuestions'
#
#    question = Column(String, primary_key=True)
#    section = Column(Integer, nullable=False)

class iComputeTest(Base):
    __tablename__ = 'iComputeTest'

    orderId = Column(Integer)
    question = Column(String, primary_key=True)
    section = Column(Integer, nullable=False)
    year = Column(Date)
    studentGrade = Column(String)

class Questions(Base):
    __tablename__ = 'Questions'

    question = Column(String, primary_key=True)
    answer = Column(String, primary_key=True)
    is_Correct = Column(boolean, nullable=False)
    sction = Column(Integer, nullable=False)
