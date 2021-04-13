from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash
from contextlib import contextmanager
from config import DATABASE_URI
from app import app
from app.database import Base
from app.models import Users, Files, Products
from config import providers

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def reset_database():
    print('Reset database')
    Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)

def create_database():
    print('Create database')
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def seed_products():
    print('Seed products')
    with session_scope() as s:
        product = Products(
            title="trainers",
            subtitle='Trainers In White',
            img='%s/assets/products/img1.jpg' % app.config['REMOTE'],
            price=76,
            rating=4.6,
            code=135234,
            hashtag="whitetrainers",
            technology=[
                    "Ollie patch",
                    "Cup soles",
                    "Vulcanized rubber soles"
                ],
            discount=None,
            description_1="Sneakers (also known as athletic shoes, tennis shoes,gym shoes, runners, takkies, or trainers) are shoes primarily designed for sports or other forms of physical exercise, but which are now also often used for everyday wear.",
            description_2="The term generally describes a type of footwear with a flexible sole made of rubber or synthetic material and an upper part made of leather or synthetic materials.",
            updatedAt=func.now()
        )
        s.add(product)

def seed_users():
    print('Seed users')
    with session_scope() as s:
        password = "password"
        password_hash = generate_password_hash(password, method='sha256')
        user = Users(
            firstName='Admin',
            email="admin@flatlogic.com",
            emailVerified=True,
            role='admin',
            provider=providers['LOCAL'],
            password=password_hash,
            updatedAt=func.now()
        )
        s.add(user)

if __name__ == '__main__':
    #reset_database()
    create_database()
    seed_products()
    seed_users()
