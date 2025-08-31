import cv2
import threading
from .camera import Camera

class CameraManager:
    def __init__(self, nb_wanted_cameras: int, max_tested_indices: int = 10):
        self.available_camera_indices: list[int] = self._detect_cameras(nb_cameras, max_tested_indices)
        self.cameras: list[Camera] = self._open_available_cameras()

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
            raise RuntimeError(f"Only found {len(cameras)} cameras, but {nb_wanted_cameras} requested.")
        
        return cameras
    
    def _open_available_cameras(self):
        """Opens all available cameras
        """
        cameras: list[Camera] = []
        for cam_idx in self.available_camera_indices:
            cameras.append(Camera(cam_idx, f"Camera Stream {cam_idx}"))
        return cameras

    def run_all_cameras(self):
        threads: list[threading.Thread] = []
        for camera in self.cameras:
            camera.start() 
            t = threading.Thread(target=camera.run)
            t.start()
            threads.append(t)

        #  wait for all cameras to finish before exiting method call
        for t in threads:
            t.join()
    

if __name__ == "__main__":
    nb_cameras = int(input("how many cameras would you like to use? "))
    cam_manager = CameraManager(nb_cameras)
    cam_manager.run_all_cameras()