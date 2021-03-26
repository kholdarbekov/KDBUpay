from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from zeep.helpers import serialize_object
import logging.config
import logging
import http.client
from flask import render_template
from . import upay_blueprint
from ..models import *


httpclient_logger = logging.getLogger("http.client")


def httpclient_logging_patch(level=logging.DEBUG):
    """Enable HTTPConnection debug logging to the logging framework"""

    def httpclient_log(*args):
        httpclient_logger.log(level, " ".join(args))

    # mask the print() built-in in the http.client module to use
    # logging instead
    http.client.print = httpclient_log
    # enable debugging
    http.client.HTTPConnection.debuglevel = 1


@upay_blueprint.route('/', methods=['GET', 'POST'])
def index():
    '''logging.config.dictConfig({
            'version': 1,
            'formatters': {
                'verbose': {
                    'format': '%(name)s: %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                },
            },
            'loggers': {
                'zeep.transports': {
                    'level': 'DEBUG',
                    'propagate': True,
                    'handlers': ['console'],
                },
            }
        })'''
    logging.basicConfig(level=logging.DEBUG)
    httpclient_logging_patch()

    session = Session()
    session.auth = HTTPBasicAuth('user', 'password')
    client = Client('wsdl_url', transport=Transport(session=session))

    # CardP2PInfo = client.get_type('ns0:cardP2PInfo')
    UserCredentials = client.get_type('ns0:UserCredentials')
    CardP2PInfoElement = client.get_element('ns0:cardP2PInfo')

    cardP2PInfoElement = CardP2PInfoElement()
    userCredentials = UserCredentials(Login='login', Password='password')

    cardP2PInfoElement.StPimsApiPartnerKey = 'XXXXXXXX'
    cardP2PInfoElement.UserCredentials = userCredentials
    cardP2PInfoElement.P2pCardNumber = 'CARD_NUMBER'
    cardP2PInfoElement.Lang = 'EN'

    # Method 1:
    result = client.service.cardP2PInfo([cardP2PInfoElement])

    # Method 2: result = client.service.cardP2PInfo(cardP2PInfoRequest=[{
    # 'StPimsApiPartnerKey':'XXXXXXXX', 'UserCredentials':{'Login':'login',
    # 'Password':'password' }, 'P2pCardNumber':'CARD_NUMBER', 'Lang':'EN' }])


    # Return JSON
    return serialize_object(result, dict)

