"""
This is the code that handles WSGI.
"""

from . import base
from ..response import DefaultResponse, REASON_PHRASES


class Request(base.Request):
    """ A WSGI request class. """
    def __init__(self, handler, environ):
        """ Initialize the request. """
        base.Request.__init__(self, handler)


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
        response.prepare()
        response_status = "{0} {1}".format(str(response.status), REASON_PHRASES.get(response.status, 'UNKNOWN'))
        response_headers = [(i, response._headers[i]) for i in response._headers]

        # Return
        start_response(response_status, response_headers)

        return [response._body]
        

        
        



