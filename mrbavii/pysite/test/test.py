from ..app import Application
from .. import response

from ..handlers.wsgi import Handler

from wsgiref.simple_server import make_server


class A(Application):
    def __init__(self, config=None):
        Application.__init__(self, config)
        self._counter = 1

    def get_response(self, request):
        r = response.Response(self._config, 200, 'text/html')
        r.sendbody("<html><head><title>Hey</title><body><b>Hello World {0}</b></body></html>".format(self._counter))
        self._counter += 1

        return r

handler = Handler(A())

httpd = make_server('', 8000, handler)
httpd.serve_forever()

