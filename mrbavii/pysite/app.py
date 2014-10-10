"""
This is the application class.
"""

from .config import Config
from .request import Request
from .response import Response, DefaultResponse
from .util import convert_to_bytes
from .compat import u

class BaseApplication(object):
    """ A base application simply reacts to the WSGI call. """

    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        raise NotImplementedError

    def fix_environ(self, environ):
        """ Perform fixes on the environment passed in. """
        pass


class BaseEchoApplication(BaseApplication):
    """ A base echo application echos back information from the __call__ method. """

    def __call__(self, environ, start_response):
        """ Build the response. """
        response = u('\r\n').join([u('{0}: {1}').format(i, environ[i]) for i in sorted(environ.keys())])
        headers = [('Content-Type', 'text/plain; charset=utf-8'),
                   ('Content-Length', str(len(response)))]

        start_response('200 OK', headers)
        return [response.encode('utf-8')]


class ProxyApplication(BaseApplication):
    """ An application that dispatches to other applications based on PATH_INFO. """

    def __init__(self, app):
        BaseApplication.__init__(self)
        self._proxy = []
        self._app = app

    def register(self, path, app):
        """ Register a path and which application it is handled by. """
        self._proxy.append(('/' + path.strip('/'), app))

    def __call__(self, environ, start_response):
        """ Handle the request and dispatch to the correct application. """
        self.fix_environ(environ)

        path_info = environ['PATH_INFO']
        for (path, app) in self._proxy:
            if path_info.startswith(path) and path_info[len(path):len(path)+1] in ('', '/'):
                if len(path):
                    environ['SCRIPT_NAME'] += path_info[:len(path)]
                    environ['PATH_INFO'] = path_info[len(path):]

                return app(environ, start_response)
        else:
            return self._app(environ, start_response)


class Application(BaseApplication):
    """ An application with configuration and routes. """

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


class EchoApplication(Application):
    """ An echo application echos back information from the get_response method.
        The difference between this and BaseEchoApplication is that the resquest
        will be parsed info a Request object.
    """

    def get_repsonse(self, request):
        pass
    
