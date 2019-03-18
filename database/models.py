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
    is_Correct = Column(Boolean, nullable=False)
    section = Column(Integer, nullable=False)


class Users(Base):
    __tablename__ = 'Users'

    Username = Column(String, primary_key=True)
    Password = Column(String, nullable=False)
    UserType = Column(String, nullable=False)
    #UserTypes Student, Grader, Supervisor.


class StudentScore(Base):
    __tablename__ = 'StudentScores'

    team_name = Column(String, primary_key=True)
    team_year = Column(String, primary_key=True)
    score = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['team_name', 'team_year'], ['StudentTeams.name', 'StudentTeams.year']),
    )
