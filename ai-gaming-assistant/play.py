import torch
import cv2
import pydirectinput
import time
import os
from vision import GameVision
from model import GamingAI

# Map AI output numbers to Keys
KEY_MAP = {
    0: None,
    1: 'space',
    2: 'right'
}

def start_ai_gameplay(stop_event):
    if not os.path.exists("smart_model.pth"):
        print("No brain found! Train the model first.")
        return

    print("Loading AI...")
    model = GamingAI(output_size=3)
    model.load_state_dict(torch.load("smart_model.pth"))
    model.eval()
    
    vision = GameVision("BlueStacks")
    print("AI taking control in 3 seconds...")
    time.sleep(3)
    
    while not stop_event.is_set():
        frame = vision.capture_frame()
        if frame is None: continue
        
        # Preprocess
        img = frame / 255.0
        img_tensor = torch.tensor(img, dtype=torch.float32).unsqueeze(0)
        
        with torch.no_grad():
            prediction = model(img_tensor)
            action_idx = torch.argmax(prediction).item()
        
        key = KEY_MAP.get(action_idx)
        if key:
            print(f"AI Action: {key}")
            pydirectinput.press(key)
        
        time.sleep(0.05) # Reaction speed delay

if __name__ == "__main__":
    import threading
    e = threading.Event()
    start_ai_gameplay(e)