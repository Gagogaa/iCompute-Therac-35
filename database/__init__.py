from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///iCompute.db', convert_unicode=True)
database_session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=engine))
Base = declarative_base()
Base.query = database_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import database.models
    Base.metadata.create_all(bind=engine)

def create_section_questions():
    import database.models

    database_session.add_all([
        SectionOneQnA(question="What is the name of the unit that helps store data in a computer?", answer="CPU", is_correct=True),
        SectionOneQnA(question="What is the name of the unit that helps store data in a computer?", answer="Input", is_correct=False),
        SectionOneQnA(question="What is the name of the unit that helps store data in a computer?", answer="Memory", is_correct=False),
        SectionOneQnA(question="What is the name of the unit that helps store data in a computer?", answer="Output", is_correct=False),
        SectionOneQnA(question="This provides a step-by-step procedure for performing a task.", answer="Keyboard", is_correct=False),
        SectionOneQnA(question="This provides a step-by-step procedure for performing a task.", answer="Algorithm", is_correct=True),
        SectionOneQnA(question="This provides a step-by-step procedure for performing a task.", answer="Internet", is_correct=False),
        SectionOneQnA(question="This provides a step-by-step procedure for performing a task.", answer="Windows", is_correct=False),
        SectionOneQnA(question="Which one of the following is not a programming language?", answer="Java", is_correct=False),
        SectionOneQnA(question="Which one of the following is not a programming language?", answer="HTML", is_correct=False),
        SectionOneQnA(question="Which one of the following is not a programming language?", answer="C++", is_correct=False),
        SectionOneQnA(question="Which one of the following is not a programming language?", answer="Binary", is_correct=True)
    ])

    database_session.commit()
