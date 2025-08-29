from flask import Flask, Response
from core.camera import Camera

class Server:
    def __init__(self, camera: Camera, host='0.0.0.0', port=5000):
        self.app = Flask(__name__)
        self.camera = camera
        self.host = host
        self.port = port

        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return '<h1>Remote Cam</h1><img src="/video_feed">'

        @self.app.route('/video_feed')
        def video_feed():
            return Response(self.camera.generate_frames(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

    def run(self, debug=True):
        self.camera.start()
        self.app.run(host=self.host, port=self.port, debug=debug)
