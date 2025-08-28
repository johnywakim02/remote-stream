import os
from core.camera import Camera

log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

cam = Camera()
cam.start()