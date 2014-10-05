"""
This is the code that handles WSGI.
"""

from . import base
from ..response import DefaultResponse, REASON_PHRASES
from ..util import convert_to_bytes


class Request(base.Request):
    """ A WSGI request class. """
    def __init__(self, config, environ):
        """ Initialize the request. """
        base.Request.__init__(self, config)


class Handler(base.Handler):
    """ A WSGI handler class. """

    def __call__(self, environ, start_response):
        """ Handle a request. """
        # Handle the request
        try:
            request = Request(self._config, environ)
        except UnicodeError:
            pass # TODO: handle
        else:
            response = self._app.get_response(request)

        if response is None:
            response = DefaultResponse(self._config, 404)


        # Prepare status and headers
        headers = response.prepare()
        response_status = "{0} {1}".format(str(response.status), response.reason)
        response_headers = [(i, headers[i]) for i in headers]

        # Return
        start_response(response_status, response_headers)

        return [convert_to_bytes(response._body, response._charset)]

