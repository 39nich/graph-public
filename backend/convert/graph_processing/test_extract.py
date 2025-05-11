import cv2
import os
from convert.graph_processing.extract_line import extract_line

image_path = "C:/Users/tantz/OneDrive/Documents/FYProject/graph-tool/backend/media/Picture1.png"

img = cv2.imread(image_path)
print("Trying to load image from:", image_path)
if img is None:
    raise ValueError("cv2.imread() failed to load the image. Make sure it's a valid image file.")


if not os.path.exists(image_path):
    raise FileNotFoundError(f"File does not exist: {image_path}")

coords = extract_line(image_path)
print(f"Extracted {len(coords)} points from main contour")