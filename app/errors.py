import traceback
import typing as t

import flask
from flask import json, jsonify, Blueprint, current_app
from werkzeug.exceptions import HTTPException, InternalServerError

from app.utils import format_exception, is_iterable_not_string, is_string_types

bp_errors = Blueprint('errors', __name__)


def format_error_content(error, debug=False):
    content = {
        'error': {
            'type': error.__class__.__name__,
            'message': error.format()
        }
    }

    if error.payload:
        content['error'].update(error.payload)
    if debug:
        content['error'].update(traceback=format_exception(error))
    return content


def format_error_response(error) -> flask.Response:
    content = format_error_content(error)
    rv = jsonify(content)
    rv.status_code = error.status_code or 500

    return rv


class BaseError(Exception):
    status_code = 400

    def _format_error_msg(self) -> str:
        pass

    def format(self) -> str:
        return self._format_error_msg()

    @property
    def payload(self) -> t.Optional[dict]:
        return self.__dict__

    def __str__(self):
        msg = self.format()
        payload = None
        if self.payload:
            try:
                payload = json.dumps(self.payload, indent=4)
            except:
                try:
                    payload = str(self.__dict__)
                except:
                    pass
        if msg and payload:
            return f"{msg}\n{payload}"
        else:
            return msg if msg else payload


@bp_errors.app_errorhandler(BaseError)
def handle_error(error):
    return format_error_response(error)


@bp_errors.app_errorhandler(HTTPException)
def handle_HTTP_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({'error': {'type': e.name, 'message': e.description}})
    response.content_type = "application/json"
    return response


@bp_errors.app_errorhandler(InternalServerError)
def handle_500(error):
    status_code = 500
    original = getattr(error, "original_exception", None)

    response = {'error': {}}

    if current_app.config['DEBUG']:
        tb = [call_string.splitlines() for call_string in traceback.format_tb(original.__traceback__)]
        tb = [val for sublist in tb for val in sublist]
        response['error'].update(type=original.__class__.__name__,
                                 message=str(original),
                                 traceback=tb)
    else:
        response['error'].update(type=error.__class__.__name__, message=error.description)
    return jsonify(response), status_code


class EntityNotFound(BaseError):
    status_code = 404

    def __init__(self, entity: str, ident, columns: t.List[str] = None):
        self.entity = entity
        self.id = ident
        if is_iterable_not_string(columns):
            self.columns = columns
        elif is_string_types(columns):
            self.columns = [columns]
        else:
            self.columns = ['id']

    def _format_error_msg(self) -> str:
        return f"entity with given {', '.join(self.columns)} doesn't exist"

    @property
    def payload(self) -> t.Optional[dict]:
        return dict(entity=self.entity, id=self.id)


class NoDataFound(BaseError):
    status_code = 404

    def __init__(self, entity):
        self.entity = entity

    def _format_error_msg(self) -> str:
        return f"No data found"
