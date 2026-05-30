import keyboard
import time
import os
import cv2
from vision import GameVision

def record_gameplay():
    vision = GameVision("BlueStacks")
    
    if not os.path.exists("training_data"):
        os.makedirs("training_data")
        
    print("Recording started... Switch to BlueStacks! Press 'esc' to stop.")
    count = 0
    
    # Define your game keys here
    # 0: Nothing, 1: Space (Jump), 2: Right (Move)
    try:
        while True:
            if keyboard.is_pressed('esc'):
                print("Recording Stopped.")
                break
                
            frame = vision.capture_frame()
            if frame is None:
                continue

            key_state = 0
            if keyboard.is_pressed('space'):
                key_state = 1
            elif keyboard.is_pressed('right'):
                key_state = 2
            
            # Save only if a key is pressed (or save everything if you want idle data)
            # Saving everything helps the AI learn when *not* to do anything.
            filename = f"training_data/frame_{count}_key_{key_state}.jpg"
            cv2.imwrite(filename, frame)
            
            count += 1
            # Rate limit to ~15 FPS to avoid filling hard drive too fast
            time.sleep(0.06) 
            
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    record_gameplay()