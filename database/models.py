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
