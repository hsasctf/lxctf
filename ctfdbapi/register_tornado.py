from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from app_register import app
import pathlib, os



import sys

if not sys.platform == 'darwin':
    os.chdir("/home/root/ctf_root/ctfdbapi/")


http_server = HTTPServer(WSGIContainer(app))
http_server.listen(4998)
IOLoop.instance().start()
