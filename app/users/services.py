import os
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from app import app, mail
from app.models import Users, Files
from app import CustomError
from app.users.db import UserDBApi
from app.auth.services import Auth
from app.serializers import UsersSchema, FilesSchema

users_schema = UsersSchema(many=True)
file_schema = FilesSchema()


# User service class
class UserService:
    def create(data: dict, current_user: Users, host: str, send_invitation_emails: bool = True) -> None:
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
            raise CustomError({'message': 'Error when creating user in database: %s\n' % str(e)})
        except Exception as e:
            print("Error occurred")
            print(str(e))
            raise CustomError({'message': 'Error occurred %s\n' % str(e)})

        if emails_to_invite and len(emails_to_invite):
            if not send_invitation_emails:
                return
        Auth.send_password_reset_email(email, host, 'invitation')

    def update(user_id: str, data: dict, current_user: Users):
        print('UserService.update()')
        print(user_id)
        try:
            UserDBApi.update(user_id, data, current_user)
        except SQLAlchemyError as e:
            print("Unable to update product to database.")
            raise CustomError({'message': 'Error when updating user in database: %s\n' % str(e)})

    def remove(user_id: str, current_user: Users):
        if current_user.id == user_id:
            raise CustomError({'message': 'Error when removing user in database: deleting himself\n'})
        if not current_user.role == 'admin':
            raise CustomError({'message': 'Error when removing user in database: forbidden action for not admin user\n'})
        user = app.session.query(Users).filter_by(id=id).first()
        print(user.lastName)
        app.session.delete(user)
        app.session.commit()

    def get_all():
        print('UserService.get_all()')
        users = app.session.query(Users)
        users = users.order_by(Users.email.asc()).all()
        print(users)
        users_dict = users_schema.dump(users)
        users_list = []
        for user_dict in users_dict:
            user = app.session.query(Users).filter_by(id=user_dict['id']).first()
            user_dict['avatars'] = []
            if len(user.avatar):
                print('avatar is not empty list')
                for file_rel in user.avatar:
                    fileId = file_rel.id
                    file = app.session.query(Files).filter_by(id=fileId).first()
                    print(file.name)
                    file_dict = file_schema.dump(file)
                    user_dict['avatars'].append(file_dict)
            users_list.append(user_dict)
