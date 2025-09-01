import cv2
import threading
import logging
from .camera import Camera
from utils.logger import setup_logger
from utils.validators import validate_bt_zero, validate_between_inclusive

MIN_TESTED_INDICES = 1
MAX_TESTED_INDICES = 15

class CameraManager:
    def __init__(self, nb_wanted_cameras: int, max_tested_indices: int = 10):
        self.logger: logging.Logger = setup_logger(self.__class__.__name__, log_file= "logs/camera_manager.log")

        self._validate_inputs(nb_wanted_cameras, max_tested_indices)
    
        self.available_camera_indices: list[int] = self._detect_cameras(nb_wanted_cameras, max_tested_indices)
        self.cameras: list[Camera] = self._open_available_cameras()

    def _validate_inputs(self, nb_wanted_cameras: int, max_tested_indices: int) -> None:
        if not validate_bt_zero(nb_wanted_cameras):
            msg: str = f"in {self.__class__.__name__}, nb_wanted_cameras needs to be positive. Provided value was {nb_wanted_cameras}"
            self.logger.error(msg)
            raise RuntimeError(msg)
        if not validate_between_inclusive(max_tested_indices, MIN_TESTED_INDICES, MAX_TESTED_INDICES):
            msg: str = f"in {self.__class__.__name__}, max_tested_indices is not within the permitted range of [{MIN_TESTED_INDICES}, {MAX_TESTED_INDICES}]. Provided value was {max_tested_indices}"
            self.logger.error(msg)
            raise RuntimeError(msg)

    def _detect_cameras(self, nb_wanted_cameras, max_tested_indices) -> list[int]:
        """
        Detects available camera indices by attempting to open video capture devices.

        Args:
            nb_wanted_cameras (int): The number of camera indices to find before stopping.
            max_tested_indices (int): The maximum number of camera indices to test.

        Returns:
            list[int]: A list of available camera indices.

        Raises:
            RuntimeError: If fewer than `nb_wanted_cameras` are found after testing `max_tested_indices`.
        """
        self.logger.info(f"searching for {nb_wanted_cameras} requested cameras")
        cameras: list[int] = []
        for i in range(max_tested_indices):
            if len(cameras) == nb_wanted_cameras:
                break
            cap = cv2.VideoCapture(i)
            try:
                if cap.isOpened():
                    cameras.append(i)
            finally:
                cap.release()
        
        if len(cameras) < nb_wanted_cameras:
            msg = f"Only found {len(cameras)} cameras, but {nb_wanted_cameras} requested."
            self.logger.error(msg)
            raise RuntimeError(msg)
        
        self.logger.info(f"requested cameras found")
        return cameras
    
    def _open_available_cameras(self):
        """Opens all available cameras
        """
        cameras: list[Camera] = []
        for cam_idx in self.available_camera_indices:
            cameras.append(Camera(cam_idx, f"Camera Stream {cam_idx}"))
        return cameras

    def start_all_cameras(self):
        for camera in self.cameras:
            camera.start()

    def stop_all_cameras(self):
        for camera in self.cameras:
            camera.stop()

    def run_all_cameras(self):
        self.logger.info("Running all Cameras")
        threads: list[threading.Thread] = []
        for camera in self.cameras:
            t = threading.Thread(target=camera.run)
            t.start()
            threads.append(t)

        #  wait for all cameras to finish before exiting method call
        for t in threads:
            t.join()

        self.logger.info("All Cameras Stopped.")
    

if __name__ == "__main__":
    nb_cameras = int(input("how many cameras would you like to use? "))
    cam_manager = CameraManager(nb_cameras)
    cam_manager.start_all_cameras()
    cam_manager.run_all_cameras()
    cam_manager.stop_all_cameras()