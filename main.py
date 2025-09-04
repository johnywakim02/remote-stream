import os
from core.camera import CameraManager
from core.server import Server
from utils.input_handlers import input_yes_no, input_from_range_int

if __name__ == "__main__":
    log_folder = "logs"
    save_folder = "saved_imgs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    cam_manager = CameraManager(2)
    server = Server(cam_manager)

    ### Probing the user for wanted behavior
    saveFlag: bool = input_yes_no("Would you like to save images periodically?", default=True)
    saveFrequency: int = None
    saveOverriteFlag: bool = None
    if saveFlag:
        saveFrequency = input_from_range_int("Please choose the periodicity at which you would like to take the pictures", {1, 3, 5, 10, 20, 30})
        saveOverriteFlag = input_yes_no("Would you like to delete all previously saved images to save space?", default = True)


    try:
        cam_manager.estimate_storage_per_hour_cam(0)
        cam_manager.estimate_storage_per_hour_cam(1)
        cam_manager.save_imgs_periodically()
        server.run(debug=False)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    finally:
        cam_manager.stop_all_cameras()