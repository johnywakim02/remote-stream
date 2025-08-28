import cv2
from typing import Optional
import logging
from utils.logger import setup_logger


class Camera:
    def __init__(self, camera_idx: int = 0, window_name: str = "Camera Stream") -> None:
        self.camera_idx: int = camera_idx
        self.window_name: str = window_name
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running : bool = False
        self.logger: logging.Logger = setup_logger(self.__class__.__name__, log_file= "logs/camera.log")
    
    def start(self) -> None:
        # Open Camera
        self.cap = cv2.VideoCapture(self.camera_idx)
        if not self.cap.isOpened():
            error_msg = f"Error: Could not open camera nb. {self.camera_idx}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)

        # Run the frame capture and display process till use interruption
        self.is_running = True
        self.logger.info("Camera started")
        print("Press 'q' to quit...")
        self.run()

    def run(self) -> None:
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
        # signal that the camera process should stop running
        self.is_running = False
        # Release the cap
        if self.cap:
            self.cap.release()
        # destroy all displayed opencv windows:
        cv2.destroyAllWindows()
        self.logger.info("Camera Stopped")

if __name__ == "__main__":
    cam = Camera()
    cam.start()
