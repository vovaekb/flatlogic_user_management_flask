from flask import Flask, request, jsonify, Response
from sqlalchemy.exc import SQLAlchemyError
import datetime
# from app.models import Employee, ActionTicket, InformationTicket, Task
from app import app

# Create custom exception class
class CustomError(Exception):
	"""Input parameter error."""

@app.errorhandler(CustomError)
def handle_custom_exception(error):
    details = error.args[0]
    resp = Response(details['message'], status=200, mimetype='text/plain')
    return resp

@app.route('/', methods=['GET'])
def index():
    return Response('Hello', status=200)

'''
@app.route('/action_tickets', methods=['GET'])
def action_tickets():
    action_tickets = app.session.query(ActionTicket).all()
    print(len(action_tickets))
    return jsonify({'action_tickets ': [ticket.serialized for ticket in action_tickets]}), 200 

@app.route('/information_tickets', methods=['GET'])
def information_tickets():
    information_tickets = app.session.query(InformationTicket).all()
    return jsonify({'information_tickets': information_tickets}), 200 


@app.route('/create_action_ticket', methods=['GET', 'POST'])
def create_action_tickets():
    data = request.get_json()
    print(data)

    date_format = "%Y-%m-%dT%H:%M:%S" # '%d.%m.%Y'
    until_date = datetime.datetime.strptime(data['until_date'], date_format)
    completion_date = datetime.datetime.strptime(data['completion_date'], date_format) if 'completion_date' in data else None 
    title = data['title']

    try:
        record = ActionTicket(
            assignee_id=data['assignee_id'],
            author_id=data['author_id'],
            until_date=until_date,
            completion_date=completion_date,
            title=title,
            priority=int(data['priority']),
            type=int(data['type']),
            text=data['text'])
        app.session.add(record)
        app.session.commit()
    except SQLAlchemyError as e:
       print("Unable to add item to database.")
       error = e.__dict__['orig']
       raise CustomError({'message': 'Error when saving rate to database: %s' % error})
    return jsonify({'message': 'Success'})


@app.route('/create_information_tickets', methods=['GET', 'POST'])
def create_information_tickets():
    pass


@app.route('/create_employee', methods=['GET', 'POST'])
def create_employee():
    data = request.get_json()
    print(data)
    return jsonify({'data': data})
'''
