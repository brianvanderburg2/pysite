"""
This is the application class.
"""

from .response import Response

class Application(object):
    """ A basic application object that parses a request and produces a response. """

    def __init__(self, config):
        """ Initialize the application with optional configuration. """
        self._config = config
        self._routes = []

    def get_response(self, request):
        pass # TODO: handle routes

    def route(self, route, fn):
        pass # TODO: register a route

