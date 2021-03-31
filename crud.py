from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import dateutil.parser as parser
from contextlib import contextmanager
from config import DATABASE_URI
#from app.models import Base
from app.models import Users, Files

Base = declarative_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
# Base.metadata.create_all(engine)

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


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

# Test data model
def test_users():
    s = Session()
    #
    # create user
    #
    #'''
    # create admin user
    '''
    with session_scope() as s:
        user = Users(
            firstName='Gail', 
            lastName = 'Siemens',
            phoneNumber = '3445633',
            email = 'zxcfx@mail.com',
            role = 'admin',
            disabled = False,
            password = 'BJH%%$ET',
            emailVerified = False,
            emailVerificationToken = 'BJHGYT%',
            # emailVerificationTokenExpiresAt = 
            passwordResetToken = 'ytrt5edt',
            # passwordResetTokenExpiresAt = Column(DateTime(timezone=True)) #, server_default=func.now())
            provider = 'SimpleTower',
            importHash = 'H&^R^4f',
            # createdAt = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
            updatedAt = func.now()
        )
        s.add(user)
    # create normal user
    with session_scope() as s:
        user = Users(
            firstName= 'Larry', # 
            lastName = 'Nollan', # 'Frank',
            phoneNumber = '363464', # '2353462',
            email = 'wsdfds@asd/com', # 
            role = 'user',
            disabled = False,
            password = 'sdfs^%', # 'xcvsdfds',
            emailVerified = True,
            emailVerificationToken = '^$^%EFGJFHG',
            # emailVerificationTokenExpiresAt = 
            passwordResetToken = 'JHE%$TDRsdf2', # 'zcvsdfsdf', 
            # passwordResetTokenExpiresAt = Column(DateTime(timezone=True)) #, server_default=func.now())
            provider = 'BrightStar', # 'Nfdgd', 
            importHash = 'VHGRD^ERD', # 'BNCGFDGFDG', 
            # createdAt = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
            updatedAt = func.now()
        )
        s.add(user)
    '''


    # add user to creators and editors
    '''
    firstName = 'Larry' # 'Gail' # 
    user = s.query(Users).filter_by(firstName=firstName).first()
    print(user.lastName)
    admin = s.query(Users).filter_by(role='admin').first()
    print(admin.lastName)
    # user.createdBy = admin
    user.updatedBy = admin
    s.add(user)
    s.commit()
    '''
    # add createdAt and updatedAt timestamps to user
    '''
    with session_scope() as s:
        firstName = 'Larry' # 'Gail' # 
        user = s.query(Users).filter_by(firstName=firstName).first()
        print(user.lastName)
        date_str = '2021-03-09T10:13:53.041Z'
        datetime_obj = parser.parse(date_str)
        user.createdAt = datetime_obj
        user.updatedAt = datetime_obj
        s.add(user)
    '''
    # get info on user 
    #'''
    with session_scope() as s:
        for user in s.query(Users).all():
            # firstName = 'Larry' # 'Gail' # 
            # user = s.query(Users).filter_by(firstName=firstName).first()
            print(user.lastName)
            print('role: ', user.role)
            order = user.order
            if not order is None: 
                print('order: ', order.amount)
            createdBy = user.createdBy
            updatedBy = user.updatedBy
            if not updatedBy is None: 
                print(updatedBy)
                print(updatedBy.lastName)
            if not createdBy is None: 
                print(createdBy)
                print(createdBy.lastName)
            print('')
    #'''
    
    # get user info avatar
    '''
    user = s.query(Users).filter_by(role='user').first()
    print(user.lastName)
    order = user.order
    print('order: ', order.amount)
    #print(user.avatar)
    '''
    #s.add(user)

def test_files():
    print('\nFiles')
    # s = Session()
    # create file
    #'''
    with session_scope() as s:
        admin = s.query(Users).filter_by(role='admin').first()
        print(admin.lastName)
        file = Files(
            name = 'card.jpg', # 'test.jpg', 
            sizeInBytes = 1520, # 2250,
            privateUrl = 'https:/sqwf/sdsdmds', #'https:/sdf/sdfds',
            publicUrl = 'https:/s2cb/s5Sds', # 'https:/s2f/sduds',
            createdBy = admin,
            updatedBy = admin,
            updatedAt = func.now()
        )
        s.add(file)
        
        file = Files(
            name = 'curaprox_perio_plus.jpg', # 'test.jpg', 
            sizeInBytes = 1220, # 2250,
            privateUrl = 'https:/sqwf/sd54v.sdmds', #'https:/sdf/sdfds',
            publicUrl = 'https:/s2cb/s5Sdssdr65v.jpg', # 'https:/s2f/sduds',
            createdBy = admin,
            updatedBy = admin,
            updatedAt = func.now()
        )
        s.add(file)
    #'''
    # set product
    '''
    with session_scope() as s:
        name = 'curaprox_perio_plus.jpg' # 'card.jpg
        file = s.query(Files).filter_by(name=name).first()
        print(file.name)
        # print(file.productId)
        # user = s.query(Users).first()
        # print(user.avatar)
        title = 'Curaprox Perio Plus+ Support zubní pasta (CHX 0,09%), 75 ml'
        product = s.query(Products).filter_by(title=title).first()
        # product = file.product
        print(product.title)
        file.product = product
        s.add(file)
    '''
    # add createdAt and updatedAt timestamps to category user
    '''
    with session_scope() as s:
        file = s.query(Files).filter_by(name='card.jpg').first()
        print(file.name)
        date_str = '2021-03-09T10:13:53.041Z'
        datetime_obj = parser.parse(date_str)
        file.createdAt = datetime_obj
        file.updatedAt = datetime_obj
        s.add(file)
    '''
    # add products to category
    # set creators and editors
    '''
    user = s.query(Users).filter_by(role='user').first()
    print(user.lastName)
    # file.userId = user.id
    # file.createdBy = user
    # file.updatedById = user.id
    file.updatedBy = user
    s.add(file)
    s.commit()
    '''
    # add user to file
    #'''
    with session_scope() as s:
        name = 'curaprox_perio_plus.jpg' # 'card.jpg
        file = s.query(Files).filter_by(name=name).first()
        print(file.name)
        user = s.query(Users).filter_by(role='user').first()
        print(user.lastName)
        file.user = user
        s.add(file)
    #'''

    # get full info on file 
    #'''
    with session_scope() as s:
        # name = 'card.jpg'
        for file in s.query(Files).all():
            # file = s.query(Files).filter_by(name=name).first() # 
            print(file.name)
            print(file.id)
            createdBy = file.createdBy
            updatedBy =  file.updatedBy
            print('privateUrl: ', file.privateUrl)
            print('publicUrl: ', file.publicUrl)
            print('sizeInBytes: ', file.sizeInBytes)
            user = file.user
            if not user is None:
                print('user: ', user.lastName)
            if not createdBy is None:
                print(createdBy)
                print('createdBy: ', createdBy.lastName)
            if not updatedBy is None:
                print(updatedBy)
                print('updatedBy: ', updatedBy.lastName)
            if not file.product is None:
                product = file.product
                print('product: ', product.title)
            print('')
    #'''


if __name__ == '__main__':
    recreate_database()
    test_users()
    #test_files()

