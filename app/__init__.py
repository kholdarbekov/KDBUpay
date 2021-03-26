import decimal
import json
from flask import Flask, render_template
'''
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
'''
from config import config


class DecimalEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o,decimal.Decimal):
            return float(o)
        super(DecimalEncoder,self).default(o)


def create_app(config_name):
    app = Flask(__name__)
    app.json_encoder = DecimalEncoder
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    '''
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    '''

    # attach routes and custom error pages here
    from .upay import upay_blueprint
    app.register_blueprint(upay_blueprint)

    return app