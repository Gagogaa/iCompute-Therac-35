"""
Contains the database classes for the application
"""
class iComputeTest(Base):
    __tablename__ = 'iComputeTest'

    question = Column(String, primary_key=True)
    #answer = Column(String, primary_key=True) Not sure if we need this as the test can pull from the questions tables
    year = Column(Date)
