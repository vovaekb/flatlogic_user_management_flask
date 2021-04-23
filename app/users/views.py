import os
from flask import render_template, Blueprint, request, Response, jsonify
from flask_cors import cross_origin
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from app import app, APP_ROOT
from app import CustomError, ValidationError, ForbiddenError, get_current_user
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

@users_blueprint.errorhandler(ValidationError)
def handle_validation_error(e):
    details = e.args[0]
    return Response(details['message'], status=400, mimetype='text/plain')

@users_blueprint.errorhandler(ForbiddenError)
def handle_forbidden_error(e):
    details = e.args[0]
    return Response(details['message'], status=403, mimetype='text/plain')

# ROUTES
@users_blueprint.route('/users', methods=['POST'])
@cross_origin(supports_credentials=True)
@get_current_user
def index_post(current_user):
    print('/users POST accepted')
    data = request.get_json()
    user_data = data['data']
    if 'disabled' in user_data and user_data['disabled'] == '':
        user_data['disabled'] = None
    if 'role' in user_data and user_data['role'] == '':
        user_data['role'] = None
    print(data)
    referrer = request.headers.get("Referer")
    # print(referrer)
    try:
        UserService.create(user_data, current_user, referrer, True)
        text = 'true'
        return Response(text, status=200)
    except SQLAlchemyError as e:
        print("Unable to add user to database.")
        app.session.rollback()
        details = e.args[0]
        return Response(details, status=555, mimetype='text/plain')

@users_blueprint.route('/users', methods=['GET'])
@cross_origin(supports_credentials=True)
def index_get():
    print('/users GET accepted')
    users = UserService.get_all()
    data = {
        'rows': users,
        'count': len(users)
    }
    return jsonify(data)

@users_blueprint.route('/users/<user_id>', methods=['PUT', 'DELETE'])
@cross_origin(supports_credentials=True)
@get_current_user
def user(current_user, user_id):
    if request.method == 'PUT':
        try:
            data = request.get_json()
            print('PUT accepted')
            print(user_id)
            print(data)
            UserService.update(user_id, data['data'], current_user)
            text = 'true'
            return Response(text, status=200)
        except SQLAlchemyError as e:
            print("Unable to update user in database.")
            app.session.rollback()
            details = e.args[0]
            return Response(details, status=555, mimetype='text/plain')
    elif request.method == 'DELETE':
        UserService.remove(user_id, current_user)
        text = 'true'
        return Response(text, status=200)

@users_blueprint.route('/users/<user_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def user_get(user_id):
    try:
        user = app.session.query(Users).filter_by(id=user_id).first()
        data = user_schema.dump(user)
        data['avatar'] = []
        if len(user.avatar):
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
        details = e.args[0]
        return Response(details, status=555, mimetype='text/plain')
    return jsonify(data)

@users_blueprint.route('/users/autocomplete', methods=['GET'])
@cross_origin(supports_credentials=True)
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
