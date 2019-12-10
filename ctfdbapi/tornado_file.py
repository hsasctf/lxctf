from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app
import pathlib, os



import sys

if not sys.platform == 'darwin':
    os.chdir("/opt/ctfdbapi/")


http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
http_server.listen(4999)
IOLoop.instance().start()
