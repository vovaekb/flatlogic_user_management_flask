from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import dateutil.parser as parser
from contextlib import contextmanager
from config import DATABASE_URI
from models import Base
from models import Users, Products, Files, Categories, Brands, Orders, Payments, ProductCategory, UsersWishlistProducts, productsMore_productsProducts 

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

    # add product to user wishlist
    '''
    firstName = 'Gail' # 'Larry
    user = s.query(Users).filter_by(firstName=firstName).first()
    print(user.lastName)
    title = 'Curaprox 5460 Ultra Soft' #  'Samsung MicroSDXC 128GB + SD adaptér'
    product = s.query(Products).filter_by(title=title).first()
    print(product.title)
    user.wishlist.append(UsersWishlistProducts(userId=user.id, productId=product.id, updatedAt=func.now()))
    s.add(user)
    s.commit()
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
            print('User wishlist')
            for product_rel in user.wishlist:
                product = s.query(Products).filter_by(id=product_rel.productId).first()
                print('- ', product.title)
            print('')
    #'''
    
    # get wishlist for user
    '''
    firstName = 'Gail' # 'Larry
    user = s.query(Users).filter_by(firstName=firstName).first()
    print(user.lastName)
    rint(user.wishlist)
    product = s.query(Products).filter_by(id=user.wishlist[0].productId).first()
    print(product.title)
    '''
    # get user info avatar
    '''
    user = s.query(Users).filter_by(role='user').first()
    print(user.lastName)
    order = user.order
    print('order: ', order.amount)
    #print(user.avatar)
    '''
    #s.add(user)

def test_categories():
    # s = Session()
    # create category
    #'''
    with session_scope() as s:
        user = s.query(Users).filter_by(role='user').first()
        print(user.lastName)
        category = Categories(
            title = "PC accessories", # "Clothes",
            importHash = "NJFGDGD", # "JVHGFH",
            createdBy = user,
            updatedAt = func.now()
        )
        s.add(category)
    #'''
    
    with session_scope() as s:
        user = s.query(Users).filter_by(role='user').first()
        print(user.lastName)
        category = Categories(
            title = "Drugstore", # "Clothes",
            importHash = "H2FHGFNN", # "NJFGDGD", # "JVHGFH",
            createdBy = user,
            updatedAt = func.now()
        )
        s.add(category)
    #'''
    # s.commit()
    # add createdAt and updatedAt timestamps to category user
    '''
    with session_scope() as s:
        title = 'Drugstore'
        category = s.query(Categories).filter_by(title=title).first()
        print(category.title)
        date_str = '2021-03-09T10:13:53.041Z'
        datetime_obj = parser.parse(date_str)
        category.createdAt = datetime_obj
        category.updatedAt = datetime_obj
        s.add(category)
    '''
    # add products to category
    '''
    with session_scope() as s:
        title = 'Drugstore'
        category = s.query(Categories).filter_by(title=title).first()
        print(category.title)
        title1 = 'Sensodyne Zubní pasta Repair&Protect 75 ml'
        product1 = s.query(Products).filter_by(title=title1).first()
        print(product1.title)
        category.products.append(ProductCategory(categoryId=category.id, productId=product1.id, updatedAt = func.now()))
        title2 = 'Curaprox 5460 Ultra Soft'
        product2 = s.query(Products).filter_by(title=title2).first()
        print(product2.title)
        category.products.append(ProductCategory(categoryId=category.id, productId=product2.id, updatedAt = func.now()))
        s.add(category)
    '''
    
    # get info for category 
    # '''
    with session_scope() as s:
        title = 'Drugstore' # 'PC accessories'
        category = s.query(Categories).filter_by(title=title).first()
        print(category.title)
        # get products
        products = category.products
        for p in products:
            product = s.query(Products).filter_by(id=p.productId).first()
            print('product: ', product.title)
    #'''

def test_brands():
    # s = Session()
    # create brand
    #'''
    with session_scope() as s:
        admin = s.query(Users).filter_by(role='admin').first()
        print(admin.lastName)
        brand = Brands(
            name = "Samsung", # "Calvin Clain",
            importHash = "BHFFHG", # "GDGFDGF",
            createdBy = admin,
            updatedAt = func.now()
        )
        s.add(brand)
    
    with session_scope() as s:
        admin = s.query(Users).filter_by(role='admin').first()
        print(admin.lastName)
        brand = Brands(
            name = "Curaprox", # "Calvin Clain",
            importHash = "KsF%gG", # "GDGFDGF",
            createdBy = admin,
            updatedAt = func.now()
        )
        s.add(brand)
    
    with session_scope() as s:
        user = s.query(Users).filter_by(role='user').first()
        print(user.lastName)
        brand = Brands(
            name = "C&A",
            importHash = "jN3MgG",
            createdBy = user,
            updatedAt = func.now()
        )
        s.add(brand)
    #'''
    # add createdAt and updatedAt timestamps to category user
    '''
    with session_scope() as s:
        name = 'Curaprox'
        brand = s.query(Brands).filter_by(name=name).first()
        print(brand.name)
        date_str = '2021-03-09T10:13:53.041Z'
        datetime_obj = parser.parse(date_str)
        brand.createdAt = datetime_obj
        brand.updatedAt = datetime_obj
        s.add(brand)
    '''
    # add products to category
    # add products to brand
    '''
    with session_scope() as s:
        name = 'Curaprox'
        brand = s.query(Brands).filter_by(name=name).first()
        print(brand.name)
        title1 = 'Curaprox 5460 Ultra Soft' # 'Samsung MicroSDXC 128GB + SD adaptér', # 'Kettle Sensor TX-$21',
        product1 = s.query(Products).filter_by(title=title1).first()
        print(product1.title)
        brand.brand_products.append(product1)
        title2 = 'Curaprox Perio Plus+ Support zubní pasta (CHX 0,09%), 75 ml', 
        product2 = s.query(Products).filter_by(title=title2).first()
        print(product2.title)
        brand.brand_products.append(product2)
        s.add(brand)
    '''
    # set creators and editors
    '''
    brand = s.query(Brands).filter_by(name='Samsung').first()
    print(brand.name)
    admin = s.query(Users).filter_by(role='admin').first()
    print(admin.lastName)
    brand.updatedBy = admin
    s.add(brand)
    '''
    
    # get products under brand
    '''
    with session_scope() as s:
        name =  'Curaprox' # 'Samsung' #
        brand = s.query(Brands).filter_by(name=name).first()
        print(brand.name)
        print(brand.brand_products)
        for product in brand.brand_products:
            print('- ', product.title)
    '''
    # get all info on brand list of creators and editors
    '''
    with session_scope() as s:
        name = 'Curaprox' # 'Samsung' # 
        brand = s.query(Brands).filter_by(name=name).first()
        print(brand.name)
        print(brand.brand_products)
        product = brand.brand_products[0]
        print('product: ', product.title)
        createdBy = brand.createdBy
        updatedBy = brand.updatedBy
        print(createdBy)
        print('createdBy: ', createdBy.lastName)
        print(updatedBy)
        print('updatedBy: ', updatedBy.lastName)
    #'''

def test_orders():
    print('\nOrders')
    # create order 
    # s = Session()
    #'''
    with session_scope() as s:
        admin = s.query(Users).filter_by(role='admin').first()
        print(admin.lastName)
        order= Orders(
            name = "Books order",
            amount = 12.5,
            status = "in cart",
            importHash = "FGDGDGDG",
            createdBy = admin,
            updatedBy = admin,
            updatedAt = func.now()
        )
        s.add(order)
    
    with session_scope() as s:
        order= Orders(
            name = "Network configuration order",
            amount = 3,
            status = "bought",
            importHash = "sGDM8GSG",
            createdBy = admin,
            updatedBy = admin,
            updatedAt = func.now()
        )
        s.add(order)
    #'''
    # add createdAt and updatedAt timestamps to category user
    '''
    with session_scope() as s:
        order = s.query(Orders).first() # .filter_by(name='Samsung')
        print(order.amount)
        date_str = '2021-03-09T10:13:53.041Z'
        datetime_obj = parser.parse(date_str)
        order.createdAt = datetime_obj
        order.updatedAt = datetime_obj
        s.add(order)
    '''
    # add products to category
    # add product to order
    '''
    with session_scope() as s:
        order = s.query(Orders).first() # .filter_by(name='Samsung')
        print(order.amount)
        product = s.query(Products).filter_by(title='Samsung MicroSDXC 128GB + SD adaptér').first()
        print(product.title)
        order.product = product
        # add user (for test, TODO: remove it)
        user = s.query(Users).filter_by(role='user').first()
        print(user.lastName)
        order.user = user
        s.add(order)
    '''
    # set creators and editors
    #'''
    # add user to order
    '''
    with session_scope() as s:
        order = s.query(Orders).first() 
        print(order.amount)
        user = s.query(Users).filter_by(role='user').first()
        print(user.lastName)
        order.user = user
        s.add(order)
    '''
    # add payment to order
    '''
    with session_scope() as s:
        order = s.query(Orders).first() 
        print(order.amount)
        payment = s.query(Payments).first()
        print(payment.amount)
        order.payment = payment 
        s.add(order)
    '''

    #'''
    # get info on order (list of creators and editors)
    #'''
    print('\nGet full info')
    with session_scope() as s:
        for order in s.query(Orders).all():
            # order = s.query(Orders).first() # .filter_by(name='Samsung')
            print(order.id)
            print(order.amount)
            status = order.status
            print('status: ', status)

            product = order.product
            if not product is None:
                print('product : ', product.title)
            createdBy = order.createdBy
            updatedBy = order.updatedBy
            if not order.user is None:
                user = order.user
                print('user: ', user.lastName)
            if not order.payment is None:
                payment = order.payment
                print('payment: ', payment.amount)
            if not createdBy is None:
                print(createdBy)
                print('createdBy: ', createdBy.lastName)
            if not updatedBy is None:
                print(updatedBy)
                print('updatedBy: ', updatedBy.lastName)
            print('')
    #'''

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

def test_products():
    # s = Session()
    # create product
    #'''
    with session_scope() as s:
        admin = s.query(Users).filter_by(role='admin').first()
        print(admin.lastName)
        product = Products(
            title = 'Curaprox Perio Plus+ Support zubní pasta (CHX 0,09%), 75 ml', 
            price = 100, # 150, # 234.0,
            discount = 10, # 15, # 23.26,
            description = 'blabla ...',
            rating = 7, # 0.3, # 0.6,
            status = "in stock", # 'out of stock', # 
            importHash = "B#B^%drN", # "NBJCGH", # "NJG%^", # "GDGFDGF",
            createdBy = admin,
            updatedAt = func.now()
        )
        s.add(product)
    
    with session_scope() as s:
        admin = s.query(Users).filter_by(role='admin').first()
        print(admin.lastName)
        product = Products(
            title = 'Curaprox 5460 Ultra Soft', # 'Samsung MicroSDXC 128GB + SD adaptér', # 'Kettle Sensor TX-$21',
            price = 130, # 150, # 234.0,
            discount = 10, # 15, # 23.26,
            description = 'blabla ...',
            rating = 4, # 0.3, # 0.6,
            status = "out of stock", # 'in stock',
            importHash = "KJNBVCN", # "NBJCGH", # "NJG%^", # "GDGFDGF",
            createdBy = admin,
            updatedAt = func.now()
        )
        s.add(product)
    
    with session_scope() as s:
        admin = s.query(Users).filter_by(role='admin').first()
        print(admin.lastName)
        product = Products(
            title = 'Sensodyne Zubní pasta Repair&Protect 75 ml',
            price = 110,
            discount = 5,
            description = 'blabla ...',
            rating = 7,
            status = "in stock", # 'out of stock', # 
            importHash = "JHF%^thf",
            createdBy = admin,
            updatedAt = func.now()
        )
        s.add(product)
    
    with session_scope() as s:
        admin = s.query(Users).filter_by(role='admin').first()
        print(admin.lastName)
        product = Products(
            title = 'Samsung MicroSDXC 128GB + SD adaptér', # 'Curaprox 5460 Ultra Soft', # # 'Kettle Sensor TX-$21',
            price = 150, # 130, # # 234.0,
            discount = 15, # 10, # 23.26,
            description = 'blabla ...',
            rating = 5, # 4, # 0.3, # 0.6,
            status = "in stock", # 'out of stock', # 
            importHash = "GDGFDGF", # "KJNBVCN", # "NBJCGH", # "NJG%^", # 
            createdBy = admin,
            updatedAt = func.now()
        )
        s.add(product)
    #'''
    
    # add brand to product
    '''
    with session_scope() as s:
        product = s.query(Products).filter_by(title='Samsung MicroSDXC 128GB + SD adaptér').first()
        print(product.title)
        # image = product.image[0]
        # print(product.image)
        # print(image.name)
        brand = s.query(Brands).filter_by(name='Samsung').first()
        print(brand.name)
        product.brand = brand
        s.add(product)
        # s.commit()
    '''
    # add createdAt and updatedAt timestamps to category user
    '''
    with session_scope() as s:
        product = s.query(Products).filter_by(title='Samsung MicroSDXC 128GB + SD adaptér').first()
        print(product.title)
        date_str = '2021-03-09T10:13:53.041Z'
        datetime_obj = parser.parse(date_str)
        product.createdAt = datetime_obj
        product.updatedAt = datetime_obj
        s.add(product)
    '''
    # add file for product
    '''
    with session_scope() as s:
        title = 'Samsung MicroSDXC 128GB + SD adaptér'
        product = s.query(Products).filter_by(title=title).first()
        file = s.query(Files).filter_by(name='card.jpg').first()
        print(file.name)
        print(product.image)
        product.image.append(file)
        s.add(product)
    '''
    
    # add category for product
    '''
    with session_scope() as s:
        product = s.query(Products).filter_by(title='Samsung MicroSDXC 128GB + SD adaptér').first()
        print(product.title)
        category = s.query(Categories).filter_by(title='PC accessories').first()
        print(category.id)
        print(category.title)
        # s.add(product)
        product.categories.append(ProductCategory(categoryId=category.id, productId=product.id, updatedAt = func.now()))
        s.add(product)
        # s.commit()
    '''
    # add order for product
    '''
    with session_scope() as s:
        product = s.query(Products).filter_by(title='Samsung MicroSDXC 128GB + SD adaptér').first()
        print(product.title)
        order = s.query(Orders).first() # .filter_by(name='Samsung')
        print(order.amount)
        product.order = order
        s.add(product)
        # s.commit()
    '''
    # get category of product
    # category = s.query(Categories).filter_by(id=product.categories[0].categoryId).first()
    # print(category.title)
    #'''
    # add product to user wishlist
    '''
    with session_scope() as s:
        product = s.query(Products).filter_by(title='Samsung MicroSDXC 128GB + SD adaptér').first()
        print(product.title)
        user = s.query(Users).filter_by(firstName='Larry').first()
        print(user.lastName)
        product.users.append(UsersWishlistProducts(userId=user.id, productId=product.id, updatedAt=func.now()))
        s.add(product)
    '''
    # add user to creators
    '''
    with session_scope() as s:
        title = 'Samsung MicroSDXC 128GB + SD adaptér', # 'Curaprox 5460 Ultra Soft' # 
        product = s.query(Products).filter_by(title=title).first()
        print(product.title)
        # admin = s.query(Users).filter_by(role='admin').first()
        # print(admin.lastName)
        user = s.query(Users).filter_by(role='user').first()
        print(user.lastName)
        product.createdBy = user # admin
        product.updatedBy = user # admin
        s.add(product)
    '''
    # add more products for product
    '''
    with session_scope() as s:
        title = 'Curaprox 5460 Ultra Soft' # 
        product = s.query(Products).filter_by(title=title).first()
        print(product.title)
        title1 = 'Sensodyne Zubní pasta Repair&Protect 75 ml'
        product1 = s.query(Products).filter_by(title=title1).first()
        print(product1.title)
        title2 = 'Samsung MicroSDXC 128GB + SD adaptér'
        product2 = s.query(Products).filter_by(title=title2).first()
        product.more_products.append(productsMore_productsProducts(productId=product.id, moreProductId=product1.id, updatedAt=func.now()))
        product.more_products.append(productsMore_productsProducts(productId=product.id, moreProductId=product2.id, updatedAt=func.now()))
        s.add(product)
    '''
    # remove first category for product
    '''
    print('removing category for product')
    with session_scope() as s:
        title='Samsung MicroSDXC 128GB + SD adaptér'
        #title = 'Kettle Sencor TJ-830'
        product = s.query(Products).filter_by(title=title).first()
        print(product.title)
        print(product.categories)
        category_id = "1e14d6a5-9e9b-41bf-a216-d8ac2ec8d8d5"
        category_rel = product.categories.filter_by(categoryId=category_id).first() # [0]
        print(category_rel.productId)
        #category_rel = s.query(ProductCategory).filter_by(categoryId=product.categories[0]).first()
        #print(category_rel.productId)
        #s.remove(category_rel)
        # print(category_rel.categoryId)
        #product.categories.remove(product.categories[0]) # category_rel)
        s.add(product)
    '''

    # get users having the product in wishlist
    '''
    title = 'Curaprox 5460 Ultra Soft' # 'Samsung MicroSDXC 128GB + SD adaptér', # 'Kettle Sensor TX-$21',
    product = s.query(Products).filter_by(title=title).first()
    print(product.title)
    print(product.users)
    userIdx = 0
    user = s.query(Users).filter_by(id = product.users[userIdx].userId).first()
    print('User: ', user.firstName)
    '''
    # get full info about products (brand, category, list of creators and editors)
    #'''
    with session_scope() as s:
        products = s.query(Products).all()
        for product in products:
            # title = 'Curaprox 5460 Ultra Soft' # 
            # title = 'Samsung MicroSDXC 128GB + SD adaptér' # 'Curaprox 5460 Ultra Soft' # ', # 'Kettle Sensor TX-$21',
            # product = s.query(Products).filter_by(title=title).first()
            print(product.title)
            print(product.id)
            print('description: ', product.description)
            print('status: ', product.status)
            print('rating: ', product.rating)
            print('discount: ', product.discount)
            print('price: ', product.price)
            brand = product.brand
            if not brand is None:
                #print(brand)
                print('brand: ', brand.name)
            # images
            print('Images')
            for image in product.image:
                print('- ', image.name)
            # order = product.order
            # print('order: ', order.amount)
            # users
            print('Users having the product in wishlist')
            if product.users.count():
                for user_rel in product.users:
                    userId = user_rel.userId
                    user = s.query(Users).filter_by(id=userId).first()
                    print('* ', user.firstName)
            # category
            # print(product.categories)
            if product.categories.count(): # len(product.categories):
                print('Categories')
                for category_rel in product.categories:
                    categoryId = category_rel.categoryId
                    # print(categoryId)
                    category = s.query(Categories).filter_by(id=categoryId).first()
                    print('- ', category.title)
            if not product.createdBy is None:
                createdBy = product.createdBy
                print('createdBy: %s (%s)' % (createdBy.lastName, createdBy.role))
            if not product.updatedBy is None:
                updatedBy = product.updatedBy
                print(updatedBy)
                print('updatedBy: %s (%s)' % (updatedBy.lastName, updatedBy.role))
            # more products
            if product.more_products.count():
                more_products = product.more_products
                print('more_products for products')
                # print(more_products)
                for more_product_rel in more_products:
                    more_product_id = more_product_rel.moreProductId
                    more_product = s.query(Products).filter_by(id=more_product_id).first()
                    print('- ', more_product.title)
            print('')
    #'''

    # get all products the product is included in product's more_products
    '''
    title = 'Samsung MicroSDXC 128GB + SD adaptér' 
    product = s.query(Products).filter_by(title=title).first()
    print('')
    print(product.title)
    product_products = product.products
    print('products for product')
    # print(product_products)
    for product_product_rel in product_products:
        product_product_id = product_product_rel.productId
        product_product = s.query(Products).filter_by(id=product_product_id).first()
        print('- ', product_product.title)
    '''

def test_payments():
    print('\nPayments')
    # create payment 
    #'''
    with session_scope() as s:
        admin = s.query(Users).filter_by(role='admin').first()
        print(admin.lastName)
        payment = Payments(
            name = "Payment 1",
            # payment_date = func.now(),
            amount = 14.5,
            importHash = "GDGFDGF",
            createdBy = admin,
            updatedBy = admin,
            updatedAt = func.now()
        )
        s.add(payment)
        
        #'''
        payment = Payments(
            name = "Payment 2",
            # payment_date = func.now(),
            amount = 5,
            importHash = "bRGD8GF",
            createdBy = admin,
            updatedBy = admin,
            updatedAt = func.now()
        )
        s.add(payment)
        #'''
    #'''
    # add payment_date, createdAt and updatedAt timestamps to category user
    '''
    with session_scope() as s:
        payment = s.query(Payments).first() # .filter_by(name=name)
        print(payment.amount)
        date_str = '2021-03-09T10:13:53.041Z'
        datetime_obj = parser.parse(date_str)
        # payment.createdAt = datetime_obj
        #payment.updatedAt = datetime_obj
        payment.payment_date = datetime_obj
        s.add(payment)
    '''
    # add order to payment
    '''
    with session_scope() as s:
        payment = s.query(Payments).filter_by(amount=5).first()
        print(payment.amount)
        order = s.query(Orders).filter_by(amount=13).first() # first() # .filter_by(name='Samsung')
        print(order.amount)
        payment.order = order
        s.add(payment)
    '''
    # get list of creators and editors
    #'''
    with session_scope() as s:
        for payment in s.query(Payments).all():
            #name = 'card.jpg'
            #payment = s.query(Payments).first() # .filter_by(name=name)
            print(payment.amount)
            print('payment_date: ', payment.payment_date)
            print('createdAt: ', payment.createdAt)
            if not payment.order is None:
                order = payment.order
                print('order: ', order.amount)
            createdBy = payment.createdBy
            updatedBy = payment.updatedBy
            if not createdBy is None:
                print(createdBy)
                print('createdBy: ', createdBy.lastName)
            if not updatedBy is None:
                print(updatedBy)
                print('updatedBy:', updatedBy.lastName)
            print('')
    #'''

if __name__ == '__main__':
    #'''
    #recreate_database()
    test_users()
    #'''
    #test_files()
    #'''
    #test_categories()
    #test_orders()
    #test_brands()
    #'''
    #test_products()
    #'''
    #test_payments()
    #'''
