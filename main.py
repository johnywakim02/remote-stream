import os
from core.camera import CameraManager
from core.server import Server

if __name__ == "__main__":
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    cam_manager = CameraManager(2)
    cam = cam_manager.cameras[1]
    server = Server(cam)

    try:
        server.run(debug=False)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    finally:
        cam.stop()