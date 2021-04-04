import os
from flask import render_template
from flask_mail import Message
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from app import app, mail, APP_ROOT
from app.models import Users, Files
#from app.auth.views import CustomError
from app import CustomError
from app.auth.notifications import EMAIL_CONFIG
from app.auth.services import Auth

class EmailSender:
    def __init__(self, email, email_type):
        self.email = email
        # self.email_type = email_type
        self.config = EMAIL_CONFIG[email_type]

    def send(self, data):
        if not EmailSender.isConfigured():
            raise CustomError({'message': 'Error when sending email: Email provider is not configured. Please configure it in config.py\n'})
        msg = Message(self.config['subject'], sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[self.email])
        msg.html = render_template(self.config['html_template'], **data)
        mail.send(msg)

    def isConfigured():
        return (app.config['MAIL_DEFAULT_SENDER'] and app.config['MAIL_SERVER'])

# User service class
class UserService:
    def create(data, current_user, host, send_invitation_emails = True):
        print('UserService.create')
        print(host)
        if current_user is None:
            current_user = Users(id=None)
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
                    createdById = current_user.id,
                    updatedById = current_user.id,
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
        try:
            user = app.session.query(Users).filter_by(id=id).first()
            if not user:
                raise CustomError({'message': 'Error when updating user in database: user not found\n'})
            print(user.lastName)
            user.firstName = data['firstName'] or None
            user.lastName = data['lastName'] or None
            user.phoneNumber = data['phoneNumber'] or None
            user.email = data['email']
            user.role = data['role'] or "user"
            user.disabled = data['disabled'] or False
            # TODO: set updatedById to current user
            user.updatedById = current_user.id
            '''
            if 'emailVerified' in data: # and not data['emailVerified'] is None:
                user.emailVerified = data['emailVerified']
            if 'emailVerificationToken' in data: # and not data['emailVerificationToken'] is None:
                user.emailVerificationToken = data['emailVerificationToken']
            user.passwordResetToken = data['passwordResetToken'] if 'passwordResetToken' in data else None
            user.provider = data['provider'] if 'provider' in data else None
            user.password = data['password'] if 'password' in data else None
            '''
            if not data['avatar'] is None:
                print('avatar is not None')
                images = data['avatar']
                image_ids = [image.id for image in user.avatar]
                query_image_ids = [image['id'] for image in images]
                # add images to user avatar
                print('add images to user avatar')
                for image in images:
                    image_id = image['id']
                    if not image_id in image_ids:
                        # Add file to DB
                        file = Files(
                            name=image['name'],
                            sizeInBytes=image['sizeInBytes'],
                            privateUrl=image['privateUrl'],
                            publicUrl=image['publicUrl'],
                            createdById=current_user.id,
                            updatedById=current_user.id,
                            updatedAt=func.now()
                        )
                        app.session.add(file)
                        app.session.flush()
                        # file = app.session.query(Files).filter_by(id=image_id).first()
                        print(file.name)
                        user.avatar.append(file)
                # remove images excluded from avatar
                print('remove images excluded')
                for image_id in image_ids:
                    if not image_id in query_image_ids:
                        file_path = os.path.join(APP_ROOT, app.config['UPLOAD_FOLDER'], file.privateUrl)
                        user.avatar.remove(file)
                        # Remove file from DB and disk
                        app.session.delete(file)
                        os.remove(file_path)
            else:
                # remove all images
                for image in user.avatar:
                    user.avatar.remove(image)
                    file_path = os.path.join(APP_ROOT, app.config['UPLOAD_FOLDER'], image.privateUrl)
                    # Remove file from DB and disk
                    app.session.delete(image)
                    os.remove(file_path)
            app.session.add(user)
            app.session.commit()
        except SQLAlchemyError as e:
            print("Unable to update product to database.")
            #error = e.__dict__['orig']
            raise CustomError({'message': 'Error when updating user in database: %s\n' % str(e)})