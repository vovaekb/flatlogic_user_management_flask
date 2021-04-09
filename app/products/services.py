import os
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from app import app, mail
from app.models import Users, Files
from app import CustomError
from app.users.db import UserDBApi
from app.auth.services import Auth
from app.serializers import ProductsSchema

class ProductService:
    def get_images():
        pass

    def get_products():
        pass

    def get_product():
        pass

    def update_roduct():
        pass

    def create_product():
        pass

    def delete_product():
        pass