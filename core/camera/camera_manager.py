import math
import cv2
import threading
import logging
import time
from .camera import Camera
from utils.logger import setup_logger
from utils.validators import validate_bt_zero, validate_between_inclusive
from utils.file_manipulator import clear_folder, get_file_size_on_disk
from utils.constants import HOUR_TO_SEC
from utils.datetime import get_date
import os

MIN_TESTED_INDICES = 1
MAX_TESTED_INDICES = 15

class CameraManager:
    def __init__(self, nb_wanted_cameras: int, max_tested_indices: int = 10, vid_folder = "saved_vids", save_folder = "saved_imgs", delete_prior_saves = True, save_interval: int = 5):
        self.logger: logging.Logger = setup_logger(self.__class__.__name__, log_file= "logs/camera_manager.log")

        self._validate_inputs(nb_wanted_cameras, max_tested_indices)
    
        self.available_camera_indices: list[int] = self._detect_cameras(nb_wanted_cameras, max_tested_indices)
        self.cameras: list[Camera] = self._open_available_cameras()
        self.start_all_cameras()
        self.delete_prior_saves = delete_prior_saves
        self.vid_folder = vid_folder
        self.save_folder = save_folder
        self.save_interval = save_interval
        if self.delete_prior_saves:
            clear_folder(self.save_folder)
        self.prep_img_saving()

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
        """Runs all cameras in different threads
        """
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
    
    def prep_img_saving(self):
        """Creates the save folder and its subfolders if they do not exist
        """
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        date = get_date()

        for camera_idx in self.available_camera_indices:
            subfolder_path = os.path.join(self.save_folder, f"{date}/camera {camera_idx}")
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)

    def prep_vid_saving(self):


    def estimate_storage_per_hour_cam(self, camera_idx: int) -> None:
        """Estimate the storage required by camera per hour

        Args:
            camera_idx (int): index of the camera to access
        """
        camera = self.cameras[camera_idx]
        frame = camera.capture_frame()
        if frame is None:
            self.logger.warning(f"Camera {camera_idx}: No frame captured. Skipping estimation.")
            return 

        # Save the image to disk
        filename = "test_image.jpg"
        cv2.imwrite(filename, frame)

        # Get actual file size in bytes
        file_size_mb = get_file_size_on_disk(filename)

        # estimate the number of images per hour
        images_per_hour = math.ceil(HOUR_TO_SEC / self.save_interval)
        # estimate hourly storage spent
        mb_per_hour = file_size_mb * images_per_hour

        print(f"Camera {camera_idx}:")
        print(f"  -> Estimated image size: {file_size_mb:.2f} MB")
        print(f"  -> Images per hour (@ every {self.save_interval}s): {images_per_hour}")
        print(f"  -> Estimated storage per hour: {mb_per_hour:.2f} MB\n")

    def estimate_storage_per_hour(self) -> None:
        for camera_idx in self.available_camera_indices:
            self.estimate_storage_per_hour_cam(camera_idx)


    def save_imgs_periodically(self) -> None:
        """
        Starts a background thread that captures and saves images from all cameras periodically.

        Images are saved every `interval` seconds into separate subfolders for each camera.
        Each image filename is timestamped with the format `HH_MM_SS.jpg`, where:
            - HH is the hour (00-23)
            - MM is the minute (00-59)
            - SS is the second (00-59)

        The saving runs in a daemon thread, so it will not block the main program from exiting.
        """
        def run_saving():
            date = get_date()
            while True:
                for idx, camera in enumerate(self.cameras):
                    frame = camera.capture_frame()
                    save_subfolder = os.path.join(self.save_folder, f"{date}/camera {idx}")
                    if frame is not None:
                        filename = time.strftime("%H_%M_%S.jpg")
                        save_file = os.path.join(save_subfolder, filename)
                        cv2.imwrite(save_file, frame)
                time.sleep(self.save_interval)
        # set the thread as a daemon thread to allow the program to shut down when the main program to exit without blocking
        t = threading.Thread(target=run_saving, daemon=True)
        t.start()


if __name__ == "__main__":
    nb_cameras = int(input("how many cameras would you like to use? "))
    cam_manager = CameraManager(nb_cameras)
    cam_manager.run_all_cameras()
    cam_manager.stop_all_cameras()