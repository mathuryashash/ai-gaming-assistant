import torch
import torch.nn as nn

class GamingAI(nn.Module):
    def __init__(self, output_size=3): 
        # output_size=3 means: [No_Action, Space, Right] (Adjust based on your game)
        super(GamingAI, self).__init__()
        
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2),
            nn.ReLU(),
            nn.Flatten()
        )
        
        # Calculate size: 224x224 image -> reduces to approx 55x55 after conv layers
        self.fc = nn.Sequential(
            nn.Linear(64 * 55 * 55, 128),
            nn.ReLU(),
            nn.Linear(128, output_size)
        )

    def forward(self, x):
        # PyTorch expects input as (Batch, Channels, Height, Width)
        x = x.permute(0, 3, 1, 2).float() 
        x = self.conv(x)
        x = self.fc(x)
        return x