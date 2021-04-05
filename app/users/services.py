import os
import datetime
from flask import render_template
from flask_mail import Message
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from app import app, mail, APP_ROOT
from app.models import Users, Files
#from app.auth.views import CustomError
from app import CustomError
from app.auth.services import Auth, generate_token
from app.services.email import EmailSender
from app.users.db import UserDBApi

# User service class
class UserService:
    def create(data, current_user, host, send_invitation_emails = True):
        print('UserService.create')
        print(host)
        emails_to_invite = []
        try:
            email = data['email']
            if email:
                # Check if user already exists
                user = app.session.query(Users).filter_by(email=data['email']).first()
                if user:
                    raise CustomError({'message': 'Error when creating user to database: user already exists\n'})

                user = Users(
                    id=data['id'] or None,
                    firstName=data['firstName'] or None,
                    lastName=data['lastName'] or None,
                    emailVerified=True,
                    phoneNumber=data['phoneNumber'] or None,
                    authenticationUid=data['authenticationUid'] or None,
                    email=data['email'],
                    role=data['role'] or "user",
                    # importHash = data['importHash'] or None,
                    # createdAt = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
                    createdById = current_user.id if not current_user is None else None,
                    createdBy = current_user,
                    updatedById = current_user.id if not current_user is None else None,
                    updatedBy = current_user,
                    updatedAt=func.now()
                )
                user.disabled = data.get('disabled', False) or False
                # if 'disabled' in data and not data['disabled'] is None:
                #    user.disabled = data['disabled']
                user.emailVerified = True
                # if 'emailVerificationToken' in data and not data['emailVerificationToken'] is None:
                #    user.emailVerificationToken = data['emailVerificationToken']
                # user.passwordResetToken = data['passwordResetToken'] if 'passwordResetToken' in data else None
                user.provider = data['provider'] if 'provider' in data else None
                user.password = data['password'] if 'password' in data else None
                app.session.add(user)
                app.session.flush()
                if not data['avatar'] is None:
                    print('image is not None')
                    images = data['avatar']
                    for image in images:
                        imageId = image['id']
                        # Add file to DB
                        file = Files(
                            name=image['name'],
                            sizeInBytes=image['sizeInBytes'],
                            privateUrl=image['privateUrl'],
                            publicUrl=image['publicUrl'],
                            updatedAt=func.now()
                        )
                        app.session.add(file)
                        app.session.flush()
                        print(file.name)
                        user.avatar.append(file)

                app.session.add(user)
                app.session.commit()
                emails_to_invite.append(email)

        except SQLAlchemyError as e:
            print("Unable to add user to database.")
            # error = e.__dict__['orig']
            raise CustomError({'message': 'Error when creating user in database: %s\n' % str(e)})  # error})
        except Exception as e:
            print("Error occurred")
            print(str(e))
            raise CustomError({'message': 'Error occurred %s\n' % str(e)})

        if emails_to_invite and len(emails_to_invite):
            if not send_invitation_emails:
                return
        Auth.send_password_reset_email(email, host, 'invitation')

    def update(data, id, current_user):
        print('UserService.update()')
        try:
            UserDBApi.update(id, data, current_user)
        except SQLAlchemyError as e:
            print("Unable to update product to database.")
            raise CustomError({'message': 'Error when updating user in database: %s\n' % str(e)})

    def remove(id, current_user):
        if current_user.id == id:
            raise CustomError({'message': 'Error when removing user in database: deleting himself\n'})
        if not current_user.role == 'admin':
            raise CustomError({'message': 'Error when removing user in database: forbidden action for not admin user\n'})
        user = app.session.query(Users).filter_by(id=id).first()
        print(user.lastName)
        app.session.delete(user)
        app.session.commit()
