import os
import datetime
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from app import app, mail, APP_ROOT
from app.models import Users, Files
from app import CustomError, ValidationError, ForbiddenError
from app.services.encoding import generate_token


# DB API classes
class UserDBApi:
    def create(data, current_user=None):
        user = Users(
            id=data.get('id', None),
            firstName=data.get('firstName', None),
            lastName=data.get('lastName', None),
            emailVerified=True,
            phoneNumber=data.get('phoneNumber', None),
            authenticationUid=data.get('authenticationUid', None),
            email=data['email'],
            role=data.get('role', 'user'),
            # importHash = data['importHash'] or None,
            createdById=current_user.id if current_user is not None else None,
            createdBy=current_user,
            updatedById=current_user.id if current_user is not None else None,
            updatedBy=current_user,
            updatedAt=func.now()
        )
        user.disabled = data.get('disabled', False)
        # user.provider = data.get('provider', None)
        user.password = data.get('password', None)
        app.session.add(user)
        app.session.flush()
        if 'avatar' in data and data['avatar'] is not None:
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
                user.avatar.append(file)

        app.session.add(user)
        app.session.commit()

    def create_from_auth(data):
        user = Users(
            firstName=data['first_name'],
            password=data['password'],
            email=data['email'],
            # authenticationUid = data['authenticationUid'],
            updatedAt=func.now()
        )
        app.session.add(user)
        app.session.flush()
        user.authenticationUid = user.id
        app.session.add(user)
        app.session.commit()
        return user

    def update(user_id: str, data: dict, current_user: Users):
        user = app.session.query(Users).filter_by(id=user_id).first()
        if not user:
            raise ValidationError({'message': 'Update user error: user not found\n'})
        user.firstName = data['firstName'] or None
        user.lastName = data['lastName'] or None
        user.phoneNumber = data['phoneNumber'] or None
        user.email = data['email']
        user.role = data['role'] or 'user'
        user.disabled = data['disabled'] or False
        user.updatedById = current_user.id
        user.updatedBy = current_user

        if data['avatar'] is not None:
            images = data['avatar']
            image_ids = [image.id for image in user.avatar]
            query_image_ids = [image['id'] for image in images]
            # add images to user avatar
            for image in images:
                image_id = image['id']
                if image_id not in image_ids:
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
                    user.avatar.append(file)
            # remove images excluded from avatar
            for image_id in image_ids:
                if image_id not in query_image_ids:
                    file = app.session.query(Files).filter_by(id=image_id).first()
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

    def generate_email_verification_token(email: str, current_user: Users = None):
        user = app.session.query(Users).filter_by(email=email).first()
        token_expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=360)
        payload = {
            'exp': token_expires_at,
            'iat': datetime.datetime.utcnow(),
            'sub': str(user.id)
        }
        token = generate_token(payload)

        user.emailVerificationToken = token
        user.emailVerificationTokenExpiresAt = token_expires_at
        # user.updatedById = current_user.id
        app.session.add(user)
        app.session.commit()
        return token

    def generate_password_reset_token(email: str, current_user: Users = None):
        user = app.session.query(Users).filter_by(email=email).first()
        token_expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=360)
        payload = {
            'exp': token_expires_at,
            'iat': datetime.datetime.utcnow(),
            'sub': str(user.id)
        }
        token = generate_token(payload)

        user.passwordResetToken = token
        user.passwordResetTokenExpiresAt = token_expires_at
        # user.updatedById  = current_user.id
        app.session.add(user)
        app.session.commit()
        return token

    def update_password(id: str, password: str, current_user: Users = None):
        user = app.session.query(Users).filter_by(id=id).first()

        user.password = password
        user.authenticationUid = user.id
        if current_user is not None:
            user.updatedById = current_user.id
        user.updatedBy = current_user
        app.session.add(user)
        app.session.commit()
        return user

    def mark_email_verified(id: str, current_user: Users = None):
        user = app.session.query(Users) \
            .filter_by(id=id) \
            .first()
        user.emailVerified = True
        user.updatedById = current_user.id if current_user is not None else None
        # user.updatedBy = current_user
        app.session.add(user)
        app.session.commit()
