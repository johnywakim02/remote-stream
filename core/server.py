from flask import Flask, request, Response, jsonify
from core.camera import Camera
from utils.logger import setup_logger
from dotenv import load_dotenv
import os

class Server:
    """
    A Flask server class to serve video streams from a Camera object.

    Attributes:
        app (Flask): The Flask application instance.
        camera (Camera): The Camera instance providing video frames.
        host (str): Host address to bind the server. Defaults to '0.0.0.0'.
        port (int): Port number for the server. Defaults to 5000.
    """
    
    def __init__(self, camera: Camera, host='0.0.0.0', port=5000):
        """
        Initializes the Server with a Camera instance and Flask app

        Args:
            camera (Camera): The Camera instance to stream video from.
            host (str, optional): The host IP address. Defaults to '0.0.0.0'.
            port (int, optional): The port to run the Flask server on. Defaults to 5000.
        """
        load_dotenv()  
        self.stream_username = os.getenv("STREAM_USERNAME")
        self.stream_password = os.getenv("STREAM_PASSWORD")

        self.logger = setup_logger(self.__class__.__name__, log_file= "logs/server.log")

        self.app = Flask(__name__)
        self.camera = camera
        self.host = host
        self.port = port

        self.setup_routes()

    def check_auth(self, username: str, password: str) -> bool:
        return username == self.stream_username and password == self.stream_password

    def authenticate(self) -> Response:
        return Response(
            'Authentication required', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        )

    def requires_auth(self, f):
        from functools import wraps

        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not self.check_auth(auth.username, auth.password):
                return self.authenticate()
            return f(*args, **kwargs)

        return decorated

    def setup_routes(self):
        """
        Sets up Flask routes for the server.

        Routes:
            /          : Simple HTML page showing the video stream.
            /video_feed: Endpoint serving MJPEG video stream.
        """
        @self.app.route('/')
        def index():
            return '<h1>Remote Cam</h1><img src="/video_feed">'

        @self.app.route('/video_feed')
        @self.requires_auth
        def video_feed():
            return Response(self.camera.generate_frames(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        
        @self.app.errorhandler(500)
        def internal_error(error):
            self.logger.error(f"Server error: {error}", exc_info=True)
            return jsonify({"error": "Internal Server Error"}), 500
        

    def run(self, debug=True):
        """
        Starts the camera and runs the Flask development server.

        Args:
            debug (bool, optional): Whether to run Flask in debug mode. Defaults to True.
        """
        self.logger.info(f"Starting server on {self.host}:{self.port} with debug={debug}")
        self.camera.start()
        self.app.run(host=self.host, port=self.port, debug=debug)

