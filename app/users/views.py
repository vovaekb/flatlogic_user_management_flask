import os
from flask import render_template, Blueprint, request, Response, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from app import app, APP_ROOT
from app import CustomError, get_current_user
from app.models import Users, Files
from app.serializers import UsersSchema, FilesSchema
from app.users.services import UserService

# CONFIG
users_blueprint = Blueprint('users', __name__) # , template_folder='templates')
user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
file_schema = FilesSchema()
files_schema = FilesSchema(many=True)


@users_blueprint.errorhandler(CustomError)
def handle_error(e):
    details = e.args[0]
    return Response(details['message'], status=200, mimetype='text/plain')

# ROUTES
@users_blueprint.route('/users', methods=['POST'])
@get_current_user
def index_post(current_user):
    print('/users POST accepted')
    data = request.get_json()
    host = request.host # request.host_url
    print(host)
    UserService.create(data, current_user, host, True)
    # TODO: Use host (http referer header for sending password reset email )
    text = 'true'
    return Response(text, status=200)

@users_blueprint.route('/users', methods=['GET'])
def index_get():
    print('/users GET accepted')
    '''
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
    '''
    users = UserService.get_all()
    data = {
        'rows': users,
        'count': len(users)
    }
    return jsonify(data)

@users_blueprint.route('/users/<user_id>', methods=['PUT', 'DELETE']) # 'GET',
@get_current_user
def user(current_user, user_id):
    if request.method == 'PUT':
        data = request.get_json()
        print('PUT accepted')
        print(user_id)
        print(data)
        UserService.update(user_id, data, current_user)
        '''
        try:
            # print('PUT accepted')
            user = app.session.query(Users).filter_by(id=user_id).first()
            if not user:
                # Throw exception userAlreadyExists
                raise CustomError({'message': 'Error when updating user in database: user not found\n' })
            print(user.lastName)

            user.firstName=data['firstName'] or None
            user.lastName = data['lastName'] or None
            user.phoneNumber = data['phoneNumber'] or None
            user.email = data['email']
            user.role = data['role'] or "user"
            user.disabled = data['disabled'] or False
            # TODO: set updatedById to current user
            # user.updatedById
            # if 'emailVerified' in data: # and not data['emailVerified'] is None:
            #     user.emailVerified = data['emailVerified']
            # if 'emailVerificationToken' in data: # and not data['emailVerificationToken'] is None:
            #     user.emailVerificationToken = data['emailVerificationToken']
            # user.passwordResetToken = data['passwordResetToken'] if 'passwordResetToken' in data else None
            # user.provider = data['provider'] if 'provider' in data else None
            # user.password = data['password'] if 'password' in data else None
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
                            name = image['name'],
                            sizeInBytes = image['sizeInBytes'],
                            privateUrl = image['privateUrl'],
                            publicUrl = image['publicUrl'],
                            #createdBy = admin,
                            #updatedBy = admin,
                            updatedAt = func.now()
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
                        file = app.session.query(Files).filter_by(id=image_id).first()
                        print(file.id)
                        print(file.name)
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
            raise CustomError({'message': 'Error when updating user in database: %s\n' % str(e)}) # error})
        '''
        text = 'true'
        return Response(text, status=200)
    elif request.method == 'DELETE':
        UserService.remove(user_id, current_user)
        text = 'true'
        return Response(text, status=200)

@users_blueprint.route('/users/<user_id>', methods=['GET'])
def user_get(user_id):
    try:
        user = app.session.query(Users).filter_by(id=user_id).first()
        data = user_schema.dump(user)
        data['avatar'] = []
        if len(user.avatar): #.count():
            print('avatar is not empty list')
            for file_rel in user.avatar:
                fileId = file_rel.id
                # print(categoryId)
                file = app.session.query(Files).filter_by(id=fileId).first()
                print(file.name)
                file_dict = file_schema.dump(file)
                data['avatar'].append(file_dict)
    except SQLAlchemyError as e:
        print("Unable to get user from database.")
        error = e.__dict__['orig']
        # raise custom error
        # raise CustomError({'message': 'Error when saving rate to database: %s' % error})
        raise CustomError({'message': 'Error when reading user in database: %s\n' % str(e)}) # error})
    return jsonify(data)

@users_blueprint.route('/users/autocomplete', methods=['GET'])
def autocomplete():
    query = str(request.args['query'])
    print(query)
    limit = int(request.args['limit'])
    print(limit)
    # get data
    if not query == '':
        search = "%{}%".format(query)
        print(search)
        users = app.session.query(Users).filter(Users.email.like(search))
    else:
        users = app.session.query(Users)
    users = users.order_by(Users.email.asc()).all()
    if not limit is None:
        users = users[:limit]
    users_dict = [{'id': user.id, 'label': user.email} for user in users]
    # print(brands_dict)
    print(users_dict)
    return jsonify(users_dict)
