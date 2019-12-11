from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app
import os



os.chdir("/srv/ctf/ctfdbapi/")


http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
http_server.listen(4999)
IOLoop.instance().start()
