import cv2
from typing import Optional
import logging
from utils.logger import setup_logger


class Camera:
    """
    Captures video from a connected camera using OpenCV.

    This class manages the initialization, live video capture, display,
    and teardown of a video stream. Pressing 'q' in the video window stops the feed.

    Attributes:
        camera_index (int): Index of the camera to use (default is 0).
        window_name (str): Title of the OpenCV display window.
        cap (Optional[cv2.VideoCapture]): OpenCV video capture object or None.
        is_running (bool): Indicates whether the camera is currently streaming.
    
    Methods:
        start(): Initializes the camera and begins streaming.
        run(): Continuously reads and displays frames until stopped.
        stop(): Releases the camera and closes the display window.
    """

    def __init__(self, camera_idx: int = 0, window_name: str = "Camera Stream") -> None:
        """Initialize the Camera instance.

        Args:
            camera_idx (int, optional): Index of the camera device. Defaults to 0.
            window_name (str, optional): Name of the OpenCV display window. Defaults to "Camera Stream".
        """
        self.camera_idx: int = camera_idx
        self.window_name: str = window_name
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running : bool = False
        self.logger: logging.Logger = setup_logger(self.__class__.__name__, log_file= "logs/camera.log")
    
    def start(self) -> None:
        """Open the video capture device and sets up capturing frames properly

        Raises:
            RuntimeError: if the camera cannot be opened
        """
        # Open Camera
        self.cap = cv2.VideoCapture(self.camera_idx)
        if not self.cap.isOpened():
            error_msg = f"Error: Could not open camera nb. {self.camera_idx}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)

        # Run the frame capture and display process till use interruption
        self.is_running = True
        self.logger.info("Camera started")

    def generate_frames(self):
        """
        Generator that yields JPEG-encoded video frames for MJPEG streaming.

        Yields:
            bytes: Multipart JPEG frame suitable for HTTP MJPEG streaming.
        """
        try:
            if not self.is_running:
                self.logger.warning("generate_frames() called, but camera is not running.")
                return
            while self.is_running:
                # read frame
                success, frame = self.cap.read()
                if not success:
                    self.logger.error("Failed to read frame")
                    self.stop() 
                # encode frame
                ret, buffer = cv2.imencode(".jpg", frame)
                if not ret:
                    self.logger.error("Failed to encode frame.")
                    continue
                frame_bytes = buffer.tobytes()
                # yield the frame
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except Exception as e:
            self.logger.warning(f"An exception occurred during frame generation: {e}")
            self.stop()


    def run(self) -> None:
        """Display video frames in a loop until the user stops the stream.

        Shows the video in a named OpenCV window. The loop continues until the
        user presses the 'q' key. Each frame is read and displayed.
        """
        print("Press 'q' to quit...")
        # while process should be running
        while self.is_running:
            # Read a frame
            ret, frame = self.cap.read()
            if not ret:
                self.logger.error("Failed to read frame")
                self.stop()
                continue
                
            """Any Processing could go here"""

            # show the frame that was read
            cv2.imshow(self.window_name, frame)

            # allow for exit through q
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()


    def stop(self) -> None:
        """Stop the video stream and release resources.

        Closes the OpenCV window and releases the video capture device.
        """
        # signal that the camera process should stop running
        self.is_running = False
        # Release the cap
        if self.cap:
            self.cap.release()
            self.logger.info("Camera Stopped")
        # destroy the opencv windows of this camera:
        cv2.destroyWindow(self.window_name)

if __name__ == "__main__":
    cam = Camera(camera_idx=1)
    cam.start()
    cam.run()
