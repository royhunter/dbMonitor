#!/usr/bin/python
import socket
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


import config




# url_post_map = {
#     '/config' : config_post
# }

# url_get_map = {
#     '/' : root_get,
#     '/version' : version_get,
#     '/config' : config_get
# }

url_post_map = {}
url_get_map  = {}

def url_get_mapping_register(path, func):
    url_get_map[path] = func

def url_post_mapping_register(path, func):
    url_post_map[path] = func

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
            print 'get url is ' + self.path
            url_get_map[self.path](self)
        except Exception, e:
            print Exception, ":" ,e
            self.reply_err()
        return

    def do_POST(self):
        try:
            url_post_map[self.path](self)
        except Exception, e:
            print Exception, ":" ,e
            self.reply_err()
        return


class dbmHttpServer():
    def __init__(self, port):
        self.port = port

    def Run(self):
        self.server = HTTPServer(('', self.port), myHandler)
        print 'Started httpserver on port ', self.port
        self.server.allow_reuse_address = True
        self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.serve_forever()
    
    def Stop(self):
        self.server.socket.close()
