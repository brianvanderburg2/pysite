"""
This is the base application class for a WSGI application
"""

class Application(object):
    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        # TODO: setup some stuff

    def onRequest(self, request):
        pass


class NestedApplication(Application):
    def __init__(self):
        Application.__init__(self)
        self._nested = []

    def register(self, path, app):
        self._nested.append((path, app))

    def __call__(self, environ, start_response):
        # TODO: determine dispatcher to handler, fix SCRIPT_NAME and PATH_INFO, call nested application

