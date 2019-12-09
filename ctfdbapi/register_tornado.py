from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from app_register import app
import pathlib, os



import sys

os.chdir("/srv/ctf/ctfdbapi/")


http_server = HTTPServer(WSGIContainer(app))
http_server.listen(4998)
IOLoop.instance().start()
