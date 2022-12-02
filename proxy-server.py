#https://levelup.gitconnected.com/how-to-build-a-super-simple-http-proxy-in-python-in-just-17-lines-of-code-a1a09192be00

import socketserver
import http.server
import urllib.request
import sys

PORT = 8889

class MyProxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print ("do_GET> ")
        sys.stdout.write('%s → %s\n' % (self.headers.get('Referer', 'NO_REFERER'), self.path))
        self.copyfile(urllib.request.urlopen(self.path), self.wfile)
        sys.stdout.flush()

httpd = socketserver.ThreadingTCPServer(('', PORT), MyProxy)
print ("Now serving at %s\n" % str(PORT))
httpd.serve_forever()
