import datetime
import enum
import uuid
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Table, Integer, ForeignKey, ARRAY
from sqlalchemy.types import Float, Numeric, String, DateTime, Date, Enum, UnicodeText, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func
from app import database

# Base = declarative_base()


Role = Enum(
    value='Role',
    names = [
        ('admin', 1), ('user', 2)
    ]
)


class Users(database.Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    firstName = Column(String(80), nullable=True)
    lastName = Column(String(175), nullable=True)
    phoneNumber = Column(String(24), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    role = Column(Enum("admin", "user", name="enum_users_role"), nullable=True, default='user') # "Role" # Role))
    disabled = Column(Boolean, nullable=False, default=False)
    password = Column(String(255), nullable=True)
    authenticationUid = Column(String(255), nullable=True)
    emailVerified = Column(Boolean, nullable=False, default=False)
    emailVerificationToken = Column(String(255), nullable=True)
    emailVerificationTokenExpiresAt = Column(DateTime(timezone=True)) #, server_default=datetime.datetime.now().strftime(date_format))
    passwordResetToken = Column(String(255), nullable=True)
    passwordResetTokenExpiresAt = Column(DateTime(timezone=True)) #, server_default=func.now())
    provider = Column(String(255), nullable=False, default="local")
    importHash = Column(String(255), nullable=True, unique=True)
    createdAt = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=False, onupdate=func.now())
    deletedAt = Column(DateTime(timezone=True))
    createdById = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    createdBy = relationship("Users", foreign_keys=[createdById], uselist=False, post_update=True)
    updatedById = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    updatedBy = relationship("Users", foreign_keys=[updatedById], uselist=False, post_update=True)
    # avatar = relationship('Files', backref='user') # , lazy='dynamic')


class Files(database.Base):
    __tablename__ = 'files'
    # id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    id = Column(UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    # belongsTo = Column(String(255))
    # belongsToId = Column(UUID(as_uuid=True), ForeignKey('users.id')) # Column(UUID)
    # belongsToColumn = Column(String(255))
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    user = relationship("Users", foreign_keys=[userId], backref="avatar")
    name = Column(String(2083), nullable=False)
    sizeInBytes = Column(Integer, nullable=True)
    privateUrl = Column(String(2083), nullable=True)
    publicUrl = Column(String(2083), nullable=False)
    createdAt = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=False,
                       onupdate=func.now())
    deletedAt = Column(DateTime(timezone=True))
    createdById = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    createdBy = relationship("Users", foreign_keys=[createdById], uselist=False)
    updatedById = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedBy = relationship("Users", foreign_keys=[updatedById], uselist=False)

class Products(database.Base):
    __tablename__ = 'products'
    id = Column(Integer,
        primary_key=True
    )
    img = Column(String)
    title = Column(String)
    subtitle = Column(String)
    price = Column(Float)
    rating = Column(Float)
    description_1 = Column(String)
    description_2 = Column(String)
    code = Column(Float)
    hashtag = Column(String)
    technology = Column(ARRAY(String))
    discount = Column(Float)
    createdAt = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=False,
                       onupdate=func.now())
    deletedAt = Column(DateTime(timezone=True))
