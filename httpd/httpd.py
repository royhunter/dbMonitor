#!/usr/bin/python
import socket
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class myHandler(BaseHTTPRequestHandler):
    def reply_ok(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)
    
    def reply_err(self):
        self.send_error(404,'Path Not Found: %s' % self.path)

    def do_GET(self):
        if self.path == '/version':
            self.reply_ok('version')
        elif self.path == '/config':
            self.reply_ok('config')
        else:
            self.reply_err();
        return

    def do_POST(self):
        if self.path == '/config':
            content_len = int(self.headers.getheader('content-length', 0))
            content = self.rfile.read(content_len)
            self.reply_ok(content)
        else:
            self.reply_err();
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
