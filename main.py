#!/usr/bin/env python3
#
# Serving live images from Raspberry Pi Camera
# 
# Based on source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming
# 

from http import server
from threading import Condition
import io
import picamera # type: ignore
import socketserver

IMG_WIDTH = 640
IMG_HEIGHT = 480

PORT = 8000

PAGE = f"""\
<html>
    <head>
        <title>Raspberry Pi - Surveillance Camera</title>
    </head>
    <body>
        <center>
            <h1>Raspberry Pi  - Camera</h1>
        </center>
        <center>
            <img src="/image.jpeg" width="{IMG_WIDTH}" height="{IMG_HEIGHT}">
        </center>
    </body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b"\xff\xd8"):
            # New frame, copy the existing buffer"s content and notify all
            # clients it"s available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(301)
            self.send_header("Location", "/index.html")
            self.end_headers()
        elif self.path == "/index.html":
            content = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == "/image.jpeg":
            self.send_response(200)
            self.send_header("Age", str(0))
            self.send_header("Cache-Control", "no-cache, private")
            self.send_header("Pragma", "no-cache")
            self.send_header("Content-Type", "image/jpeg")
            with output.condition:
                output.condition.wait()
                frame = output.frame
            self.send_header("Content-Length", str(len(frame))) # type: ignore
            self.end_headers()
            self.wfile.write(frame) # type: ignore
            self.wfile.write(b"\r\n")
            return
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution=f"{IMG_WIDTH}x{IMG_HEIGHT}", framerate=10) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format="mjpeg")
    try:
        address = ("", PORT)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()

