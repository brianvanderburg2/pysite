"""
This is the application class.
"""

from .config import Config
from .request import Request
from .response import Response, DefaultResponse
from .util import convert_to_bytes

class BaseApplication(object):
    """ A base application simply reacts to the WSGI call. """
    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        raise NotImplementedError

class Application(BaseApplication):
    """ An application with configuration and routs. """

    _default_config = {
        'server.request.uploads.enabled': False,
        'server.request.uploads.max_size': 1024000,
        'server.request.uploads.max_count': 1,
        'server.response.default.content_type': 'application/octet-stream',
        'server.response.default.encoding': 'utf-8'
    }

    def __init__(self, config):
        BaseApplication.__init__(self)
        self._config = Config(self._default_config, config)
        self._routes = []
    
    def get_response(self, request):
        pass # TODO: handle routes

    def route(self, route, fn):
        pass # TODO: register a route

    def __call__(self, environ, start_response):
        """ Handle the application call. """
        # Handle the request
        try:
            request = Request(self._config, environ)
        except UnicodeError:
            pass # TODO: handle
        else:
            response = self.get_response(request)

        if response is None:
            response = DefaultResponse(self._config, 404)


        # Prepare status and headers
        headers = response.prepare()
        response_status = "{0} {1}".format(str(response.status), response.reason)
        response_headers = [(i, headers[i]) for i in headers]

        # Return
        start_response(response_status, response_headers)

        return [convert_to_bytes(response._body, response._charset)]


