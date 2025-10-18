# train_yolo.py
"""
Train YOLO model on rose leaf disease dataset
- Uses YOLOv5 (PyTorch hub)
- Dataset must be in YOLO format (images + labels)
"""

import torch


data_yaml = 'dataset.yaml'  # YAML config for YOLO dataset
# Load YOLOv5 model from PyTorch hub
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt', force_reload=True)

# Training parameters
epochs = 50
batch_size = 16

# Train
model.train(data=data_yaml, epochs=epochs, batch_size=batch_size)

# Save best weights
model.save('yolov5_rose_best.pt')
print("YOLO training complete. Weights saved as yolov5_rose_best.pt")
