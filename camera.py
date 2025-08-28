import cv2

class Camera:
    def __init__(self, camera_idx: int = 0, window_name: str = "Camera Stream") -> None:
        self.camera_idx: int = camera_idx
        self.window_name: str = window_name
        self.cap: cv2.VideoCapture = None
        self.is_running : bool = False
    
    def start(self) -> None:
        # Open Camera
        self.cap = cv2.VideoCapture(self.camera_idx)
        if not self.cap.isOpened():
            raise RuntimeError(f"Error: Could not open camera nb. {self.camera_idx}")

        # Run the frame capture and display process till use interruption
        self.is_running = True
        print("Camera started. Press `q` to quit...")
        self.run()

    def run(self) -> None:
        # while process should be running
        while self.is_running:
            # Read a frame
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read frame")
                self.stop()
                continue
                
            ### Any Processing could go here

            # show the frame that was read
            cv2.imshow(self.window_name, frame)

            # allow for exit through q
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()


    def stop(self) -> None:
        # signal that the camera process should stop running
        self.is_running = False
        # Release the cap
        if self.cap:
            self.cap.release()
        # destroy all displayed opencv windows:
        cv2.destroyAllWindows()
        print("Camera Stopped")
        

if __name__ == "__main__":
    cam = Camera()
    cam.start()
