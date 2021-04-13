from sqlalchemy import create_engine
from config import DATABASE_URI
from app.database import Base

engine = create_engine(DATABASE_URI)


def reset_database():
    print('Reset database')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def create_database():
    print('Create database')
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_database()

