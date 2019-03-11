"""
Contains the database classes for the application
"""
class iComputeTest(Base):
    __tablename__ = 'iComputeTest'

    id = Column(Integer, primary_key=True)
    SecOneQuestion = Column(String)
    SecTwoNThreeQuestion =Column(String)
    year = Column(Date)
    studentGrade = Column(String)
