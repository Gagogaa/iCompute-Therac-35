"""
Contains the database classes for the application
"""


from sqlalchemy import Column, Boolean, String, Integer, Date, ForeignKeyConstraint
from database import Base


class StudentTeam(Base):
    __tablename__ = 'StudentTeams'

    team_name = Column(String, primary_key=True)
    team_year = Column(Integer, primary_key=True)
    school_name = Column(String, nullable=False)



class StudentAnswer(Base):
    __tablename__ = 'StudentAnswers'

    team_name = Column(String, primary_key=True)
    team_year = Column(Integer, primary_key=True)
    section = Column(Integer, nullable=False)
    question = Column(String, primary_key=True)
    answer = Column(String)

    __table_args__ = (
        ForeignKeyConstraint(['team_name', 'team_year'], ['StudentTeams.team_name', 'StudentTeams.team_year']),
    )


class iComputeTest(Base):
    __tablename__ = 'iComputeTest'

    orderId = Column(Integer)
    question = Column(String, primary_key=True)
    section = Column(Integer, nullable=False)
    year = Column(Integer)
    student_grade = Column(String)

    __table_args__ = (
        ForeignKeyConstraint(['question'], ['Questions.question']),
    )

class Questions(Base):
    __tablename__ = 'Questions'

    question = Column(String, primary_key=True)
    answer = Column(String, primary_key=True)
    is_correct = Column(Boolean, nullable=False)
    section = Column(Integer, nullable=False)


class Users(Base):
    __tablename__ = 'Users'

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    #UserTypes Student, Grader, Supervisor.


class StudentScore(Base):
    __tablename__ = 'StudentScores'

    team_name = Column(String, primary_key=True)
    team_year = Column(String, primary_key=True)
    total_score = Column(Integer, nullable=False)
    section_one_score = Column(Integer, nullable=False)
    section_two_score = Column(Integer)
    section_three_score = Column(Integer)
    #Left section one and two as nullable to allow for
    #full release at end of sprint 3 will update as necessary
    __table_args__ = (
        ForeignKeyConstraint(['team_name', 'team_year'], ['StudentTeams.team_name', 'StudentTeams.team_year']),
    )
