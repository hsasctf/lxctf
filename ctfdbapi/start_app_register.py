from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from app_register import app
import pathlib, os

import sys

# runs the app using the WSGI framework on the Tornado HTTP server

if not sys.platform == 'darwin':
    os.chdir("/home/ctf/lxctf/ctfdbapi/")



http_server = HTTPServer(WSGIContainer(app))
# it starts an http server on the given port
http_server.listen(4998)
# hat mit multi thread zu tun was eine bestimmten thread zurück liefert
# starts more processes which share the same port
IOLoop.instance().start()

# Starts the registration Website
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4998, debug=True)
