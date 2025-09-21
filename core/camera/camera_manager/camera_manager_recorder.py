import os

from utils.datetime import get_date
from utils.file_manipulator import clear_folder

class CameraManagerRecorder:
    def __init__(self, save_fps = 10, vid_folder = "saved_vids", save_folder = "saved_imgs", delete_prior_saves = True, save_interval: int = 5):
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