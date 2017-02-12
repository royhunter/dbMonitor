#!/usr/bin/python
import socket
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


def version_get(myHttpHandler):
    myHttpHandler.reply_ok(myHttpHandler.path)

def config_get(myHttpHandler):
    myHttpHandler.reply_ok(myHttpHandler.path)

def config_post(myHttpHandler):
    content_len = int(myHttpHandler.headers.getheader('content-length', 0))
    content = myHttpHandler.rfile.read(content_len)
    myHttpHandler.reply_ok(content)

url_post_map = {
    '/config' : config_post
}

url_get_map = {
    '/version' : version_get,
    '/config' : config_get
}

class myHandler(BaseHTTPRequestHandler):

    def version_handle(self):
        self.reply_ok('version')

    def config_handle(self):
        self.reply_ok('config')

    def reply_ok(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)
    
    def reply_err(self):
        self.send_error(404,'Path Not Found: %s' % self.path)

    def do_GET(self):
        try:
            url_get_map[self.path](self)
        except:
            self.reply_err()
        return

    def do_POST(self):
        try:
            url_post_map[self.path](self)
        except:
            self.reply_err()
        return


class dbmHttpServer():
    def __init__(self, port):
        self.port = port

    def Run(self):
        try:
            server = HTTPServer(('', self.port), myHandler)
            print 'Started httpserver on port ', self.port
            server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.serve_forever()
        except KeyboardInterrupt:
            print '^C received, shutting down the web server'
            server.socket.close()
