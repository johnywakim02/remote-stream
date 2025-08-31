import cv2

class CameraManager:
    def __init__(self, nb_wanted_cameras: int, max_tested_indices: int = 10):
        self.available_camera_indices: list[int] = self._detect_cameras(nb_cameras, max_tested_indices)

    def _detect_cameras(self, nb_wanted_cameras, max_tested_indices) -> list[int]:
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
    
    def get_available_camera_indices(self) -> list[int]:
        """Return a list of indices of detected cameras."""
        return self.available_camera_indices
    

if __name__ == "__main__":
    nb_cameras = int(input("how many cameras would you like to use? "))
    cam_manager = CameraManager(nb_cameras)
    available_camera_indices = cam_manager.get_available_camera_indices()
    print(available_camera_indices)