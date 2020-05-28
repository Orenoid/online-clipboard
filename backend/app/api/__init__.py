from flask import Blueprint
from flask_cors import CORS
from flask_restplus import Api

from app.api.controller.clip import Clips, ChannelClips
from app.api.error import handle_uncaught_exception, CustomHTTPError, handle_custom_http_error

api_bp = Blueprint('api', __name__)
CORS(api_bp)

# error handler
api_bp.register_error_handler(CustomHTTPError, handle_custom_http_error)
api_bp.register_error_handler(Exception, handle_uncaught_exception)

api = Api(api_bp, version='1.0')

api.add_resource(Clips, '/clips')
api.add_resource(ChannelClips, '/channel/clips')
