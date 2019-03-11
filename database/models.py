"""
Contains the database classes for the application
"""
class iComputeTest(Base):
    __tablename__ = 'iComputeTest'

    question = Column(String, primary_key=True)
    answer = Column(String, primary_key=True)
    year = Column(Date)
    
