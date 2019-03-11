"""
Contains the database classes for the application
"""
class iComputeTest(Base):
    __tablename__ = 'iComputeTest'

    id = Column(Integer, primary_key=True)
    SecOneQuestion = Column(String)
    SecTwoNThreeQuestion =Column(String)
    #answer = Column(String, primary_key=True) Not sure if we need this as the test can pull from the questions tablesg
    year = Column(Date)
    studentGrade = Column(String)
