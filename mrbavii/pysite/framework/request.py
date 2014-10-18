"""
This is the code providing request.
"""

import time

from .config import Config

class BaseRequest(object):
    """ A base request class. """
    def __init__(self, config, environ):
        """ Initialize the request object. 
            
            Parameters:

                config -- The configuration object.
        """
        self._config = config
        self._timer = time.time()

    def clock(self):
        """ Determine the time of the request so far. """
        return time.clock() - self._timer

class Request(BaseRequest):
    """ A request object. """
    pass
