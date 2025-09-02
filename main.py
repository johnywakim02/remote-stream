import os
from core.camera import CameraManager
from core.server import Server

if __name__ == "__main__":
    log_folder = "logs"
    save_folder = "saved_imgs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    cam_manager = CameraManager(2)
    server = Server(cam_manager)

    try:
        cam_manager.save_imgs_periodically()
        server.run(debug=False)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    finally:
        cam_manager.stop_all_cameras()