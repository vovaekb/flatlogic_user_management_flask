import datetime
from flask import Flask, request, jsonify, Response

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
