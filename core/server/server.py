from flask import Flask, Response, jsonify, render_template
from core.camera import CameraManager
from .server_auth import ServerAuth
from utils.logger import setup_logger
from dotenv import load_dotenv
import os

class Server:
    """
    A Flask server class to serve video streams from a Camera object.

    Attributes:
        app (Flask): The Flask application instance.
        camera_manager (CameraManager): The CameraManager instance providrd cameras with can generate video frames.
        host (str): Host address to bind the server. Defaults to '0.0.0.0'.
        port (int): Port number for the server. Defaults to 5000.
    """
    
    def __init__(self, camera_manager: CameraManager, host='0.0.0.0', port=5000):
        """
        Initializes the Server with a Camera instance and Flask app

        Args:
            camera_manager (CameraManager): The CameraManager instance to access available cams and stream videos from.
            host (str, optional): The host IP address. Defaults to '0.0.0.0'.
            port (int, optional): The port to run the Flask server on. Defaults to 5000.
        """
        load_dotenv()
        correct_username = os.getenv("STREAM_USERNAME")
        correct_password = os.getenv("STREAM_PASSWORD")
        self.auth = ServerAuth(correct_username=correct_username, correct_password=correct_password)

        self.logger = setup_logger(self.__class__.__name__, log_file= "logs/server.log")

        self.app = Flask(__name__)
        self.camera_manager = camera_manager
        self.host = host
        self.port = port

        self.setup_routes()


    def setup_routes(self):
        """
        Sets up Flask routes for the server.

        Routes:
            /          : Simple HTML page showing the video stream.
            /video_feed: Endpoint serving MJPEG video stream.
        """
        @self.app.route('/')
        @self.auth.requires_auth
        def index():
            cameras = list(range(len(self.camera_manager.cameras)))
            return render_template('index.html', cameras=cameras)


        @self.app.route('/video_feed/<int:camera_id>')
        @self.auth.requires_auth
        def video_feed(camera_id):
            try:
                camera = self.camera_manager.cameras[camera_id]
            except IndexError:
                return jsonify({"error": "Camera not found"}), 404

            return Response(
                camera.generate_frames(),
                mimetype='multipart/x-mixed-replace; boundary=frame'
            )
        
        @self.app.errorhandler(500)
        def internal_error(error):
            self.logger.error(f"Server error: {error}", exc_info=True)
            return jsonify({"error": "Internal Server Error"}), 500
        

    def run(self, debug=True):
        """
        Starts all cameras from manager and runs the Flask development server.

        Args:
            debug (bool, optional): Whether to run Flask in debug mode. Defaults to True.
        """
        self.logger.info(f"Starting server on {self.host}:{self.port} with debug={debug}")
        self.camera_manager.start_all_cameras()
        self.app.run(host=self.host, port=self.port, debug=debug)

