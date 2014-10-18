from ..app import Application, ProxyApplication, BaseEchoApplication
from .. import response
from ..config import Config

from wsgiref.simple_server import make_server


c = Config()

class A(Application):
    def __init__(self, config):
        Application.__init__(self, config)
        self._counter = 1

    def get_response(self, request):
        r = response.Response(self._config, 'text/html', charset="utf-8")
        r.sendbody("<html><head><title>Hey</title><body><b>Hello World {0}:{1}</b></body></html>".format(self._counter, request._timer))
        self._counter += 1

        return r

p = ProxyApplication(BaseEchoApplication())
p.register('/1test', A(c))
p.register('/2test', BaseEchoApplication())

httpd = make_server('', 8000, p)
httpd.serve_forever()

