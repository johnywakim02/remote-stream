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


    ### Probing the user for wanted behavior
    nb_wanted_cameras: int = input_from_range_int("please enter the number of USB cameras you want to use", {1,2,3,4,5,6,7,8,9,10})
    save_flag: bool = input_yes_no("Would you like to save images periodically?", default=True)
    save_interval: int = 0
    save_overrite_flag: bool = False
    if save_flag:
        save_interval = input_from_range_int("Please choose the periodicity at which you would like to take the pictures", {1, 3, 5, 10, 20, 30})
        save_overrite_flag = input_yes_no("Would you like to delete all previously saved images to save space?", default = True)

    cam_manager = CameraManager(nb_wanted_cameras=nb_wanted_cameras, delete_prior_saves=save_overrite_flag, save_interval= save_interval)
    server = Server(cam_manager)

    try:
        if save_flag:
            cam_manager.estimate_storage_per_hour()
            cam_manager.estimate_vid_storage_per_hour()
            cam_manager.save_imgs_periodically()
        server.run(debug=False)
    except KeyboardInterrupt:
        pass
    finally:
        cam_manager.stop_all_cameras()