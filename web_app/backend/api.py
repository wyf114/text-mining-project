"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from flask import Blueprint, request, jsonify
from models import db

api = Blueprint('api', __name__)

###################################################
"""
API 1 - 
"""