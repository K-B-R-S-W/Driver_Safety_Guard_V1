from google.colab import drive
drive.mount('/content/drive')

path = '/content/drive/MyDrive/roboflow data set for drowsiness'

import zipfile
import os

# Define the path to the zip file
zip_file_path = "/content/drive/MyDrive/roboflow data set for drowsiness/drowsiness.v10i.yolov8 (2).zip"

# Define the directory where you want to extract the contents
extracted_dir_path = "/content/extracted"

# Create the directory if it doesn't exist
if not os.path.exists(extracted_dir_path):
    os.makedirs(extracted_dir_path)

# Extract the contents of the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_dir_path)

print("Extraction complete.")

!pwd

%cd /content/extracted

%cd /content/extracted

!yolo task=detect mode=train model=yolov8m.pt data= data.yaml epochs=100 imgsz=640 plots=True

import shutil
import os

# Define source and destination paths
source_path = "/content/extracted/runs/detect/train"
destination_path = "/content/drive/MyDrive/roboflow data set for drowsiness"

# Join the destination path with the base name of the source directory
destination_path = os.path.join(destination_path, os.path.basename(source_path))

# Copy the directory contents to the destination folder
shutil.copytree(source_path, destination_path)

print("Directory contents copied successfully to the destination folder.")