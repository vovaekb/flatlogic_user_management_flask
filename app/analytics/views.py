from flask import render_template, abort, Blueprint, jsonify
from flask_cors import cross_origin
from app import app
from app.mocks import mock

analytics_blueprint = Blueprint('analytics', __name__) #, template_folder='templates')

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@analytics_blueprint.route('/analytics', methods=['GET'])
@cross_origin(supports_credentials=True)
def index():
    return jsonify(mock['analytics'])