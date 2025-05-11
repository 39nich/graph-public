import cv2
from typing import List, Tuple
#import matplotlib.pyplot as plt
    #plt.imshow(edges, cmap='gray')
    #plt.show()
    
def extract_line(image_path: str) -> List[Tuple[int, int]]:
    """
    Extract the graph line from an image as a list of (x,y) pixel coordinates

    Function Param:
        image_path (str): A string containing the path to the image file.

    Returns:
        List[Tuple[int, int]]: The pixel coordinates of the graph line
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image at path: {image_path}")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Found {len(contours)} contours.")
    for i, contour in enumerate(contours):
        print(f"Contour {i}: {len(contour)} points")

    main_contour = max(contours, key=cv2.contourArea)

    pixel_coords = []

    for point in main_contour:
        x, y = point[0]
        pixel_coords.append((int(x), int(y)))

    print("Sampled pixel coordinates (first 10):", pixel_coords[:10])
    return pixel_coords    


