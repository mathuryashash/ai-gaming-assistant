import cv2
import numpy as np
import mss
import pygetwindow as gw

class GameVision:
    def __init__(self, window_name="BlueStacks App Player"):
        self.window_name = window_name
        self.sct = mss.mss()

    def get_window_geometry(self):
        # specific logic to find the BlueStacks window
        try:
            windows = gw.getWindowsWithTitle(self.window_name)
            if not windows:
                print(f"Window '{self.window_name}' not found! Is BlueStacks open?")
                return None
            
            window = windows[0]
            # Create a dict for MSS (top, left, width, height)
            return {"top": window.top, "left": window.left, "width": window.width, "height": window.height}
        except Exception as e:
            print(f"Error finding window: {e}")
            return None

    def capture_frame(self):
        monitor = self.get_window_geometry()
        if not monitor: return None

        # Capture the screen region
        try:
            img = np.array(self.sct.grab(monitor))
            
            # Convert BGRA to RGB (BlueStacks usually gives BGRA)
            img = img[:, :, :3]
            
            # Resize to 224x224 (Standard size for AI models)
            small_img = cv2.resize(img, (224, 224))
            
            return small_img
        except Exception as e:
            print(f"Screen capture failed: {e}")
            return None

# Quick test to see if it works
if __name__ == "__main__":
    v = GameVision()
    while True:
        frame = v.capture_frame()
        if frame is not None:
            cv2.imshow("AI Eyes", frame)
        if cv2.waitKey(1) == ord('q'):
            break