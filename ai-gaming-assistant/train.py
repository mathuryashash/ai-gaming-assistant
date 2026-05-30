import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import cv2
import os
import glob
from model import GamingAI

class GameData(Dataset):
    def __init__(self, data_dir):
        self.file_list = glob.glob(os.path.join(data_dir, "*.jpg"))
        
    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        img_path = self.file_list[idx]
        img = cv2.imread(img_path)
        img = img / 255.0 # Normalize
        
        # Parse label from filename: "frame_0_key_1.jpg" -> 1
        filename = os.path.basename(img_path)
        try:
            key_state = int(filename.split("_")[-1].split(".")[0])
        except:
            key_state = 0
        
        return torch.tensor(img, dtype=torch.float32), torch.tensor(key_state, dtype=torch.long)

def train_model_logic():
    print("Checking for training data...")
    if not os.path.exists("training_data") or not os.listdir("training_data"):
        print("No data found! Record some gameplay first.")
        return "No Data"

    dataset = GameData("training_data")
    loader = DataLoader(dataset, batch_size=16, shuffle=True)
    
    model = GamingAI(output_size=3) 
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    print("Training Started (This may take a while)...")
    epochs = 5 
    
    for epoch in range(epochs):
        total_loss = 0
        for images, labels in loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(loader):.4f}")

    torch.save(model.state_dict(), "smart_model.pth")
    print("Model Saved.")
    return "Success"

if __name__ == "__main__":
    train_model_logic()