from flask import Blueprint

upay_blueprint = Blueprint('upay', __name__)

from . import views, errors