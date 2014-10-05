"""
This is the code providing a base request, response, and handler.
"""

import time

from ..config import Config

class Request(object):
    """ A base request class. """
    def __init__(self, config):
        """ Initialize the request object. 
            
            Parameters:

                config -- The configuration object.
        """
        self._config = config
        self._timer = time.clock()

    def clock(self):
        """ Determine the time of the request so far. """
        return time.clock() - self._timer


class Handler(object):
    """
        A handler object process requests from a server in a particular fashion
        and calls the application, then handles the response from the application
        as needed by the server.
    """
    _default_config = {
        'server.request.uploads.enabled': False,
        'server.request.uploads.max_size': 1024000,
        'server.request.uploads.max_count': 1,
        'server.response.default.content_type': 'application/octet-stream',
        'server.response.default.encoding': 'utf-8'
    }

    def __init__(self, app, config=None):
        """ Initialize a handler object. 
            
            Paramteters:

                app -- The application that gets called for each request.
                config -- The configuration for the handler, request, and response.
        """
        self._app = app
        self._config = Config(self._default_config, config)


