import logging
import math
import os
import time

import cv2

from core.camera import Camera
from utils.constants import BYTE_TO_MB, HOUR_TO_SEC
from utils.datetime import get_date
from utils.file_manipulator import clear_folder, get_file_size_on_disk
from utils.logger import setup_logger

class CameraManagerRecorder:
    def __init__(self, save_fps = 10, vid_folder = "saved_vids", save_folder = "saved_imgs", delete_prior_saves = True, save_interval: int = 5):
        self.logger: logging.Logger = setup_logger(self.__class__.__name__, log_file= "logs/camera_manager_recorder.log")
        self.delete_prior_saves = delete_prior_saves
        self.save_fps = save_fps
        self.vid_folder = vid_folder
        self.save_folder = save_folder
        self.save_interval = save_interval
        if self.delete_prior_saves:
            clear_folder(self.save_folder)

    def prep_img_saving(self, available_camera_indices):
        """Creates the save folder and its subfolders if they do not exist
        """
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        date = get_date()

        for camera_idx in available_camera_indices:
            subfolder_path = os.path.join(self.save_folder, f"{date}/camera {camera_idx}")
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)

    def prep_vid_saving(self, available_camera_indices):
        if not os.path.exists(self.vid_folder):
            os.makedirs(self.vid_folder)

        date = get_date()
        
        for camera_idx in available_camera_indices:
            subfolder_path = os.path.join(self.vid_folder, f"{date}/camera {camera_idx}")
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)

    def estimate_storage_per_hour_cam(self, camera: Camera) -> None:
        """Estimate the storage required by camera per hour

        Args:
            camera (Camera): the camera to access
        """
        frame = camera.capture_frame()
        if frame is None:
            self.logger.warning(f"Camera {camera.camera_idx}: No frame captured. Skipping estimation.")
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

        print(f"Camera {camera.camera_idx}:")
        print(f"  -> Estimated image size: {file_size_mb:.2f} MB")
        print(f"  -> Images per hour (@ every {self.save_interval}s): {images_per_hour}")
        print(f"  -> Estimated storage per hour: {mb_per_hour:.2f} MB\n")

        # Clean up test file
        os.remove(filename)

    def estimate_vid_storage_per_hour_cam(self, camera: Camera, estimation_duration_sec = 5) -> None:
        frame = camera.capture_frame()
        if frame is None:
            self.logger.warning(f"Camera {camera.camera_idx}: No frame captured. Skipping estimation.")
            return 
        
        height, width = frame.shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  
        test_filename = f"test_cam_{camera.camera_idx}.avi"
        out = cv2.VideoWriter(test_filename, fourcc, self.save_fps, (width, height))

        start_time = time.time()
        while time.time() - start_time < estimation_duration_sec:
            frame = camera.capture_frame()
            if frame is not None:
                out.write(frame)
            time.sleep(1 / self.save_fps)

        out.release()

        # Get file size in MB
        file_size_mb = os.path.getsize(test_filename) * BYTE_TO_MB

        # Estimate per hour
        estimated_hourly_mb = (file_size_mb / estimation_duration_sec) * HOUR_TO_SEC

        # Clean up test file
        os.remove(test_filename)

        print(f"Camera {camera.camera_idx}:")
        print(f"  -> Estimated video size per hour: {estimated_hourly_mb:.2f} MB")