# -*- coding: utf-8 -*-
"""
Modified on Mon Nov 20 2024
@author: UOU
"""

import cv2
import numpy as np
import os

# Parameters for drawing
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial x, y coordinates of the region

# List to store segmentation points
annotations = []

# Mouse callback function to draw contours
def draw_contour(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        annotations.append([(x, y)])  # Start a new contour

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # Add points to the current contour
            annotations[-1].append((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # Close the contour by connecting the last point to the first
        annotations[-1].append((x, y))

# Function to display the image and collect annotations
def segment_images(image_paths):
    global annotations  # Use the global annotation list

    current_image_index = 0  # Start with the first image

    while current_image_index < len(image_paths):
        image_path = image_paths[current_image_index]

        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Image not found: {image_path}")
            current_image_index += 1
            continue

        # Create a clone of the image for annotation display
        annotated_image = image.copy()
        cv2.namedWindow("Image Segmentation")
        cv2.setMouseCallback("Image Segmentation", draw_contour)

        while True:
            # Show the annotations on the cloned image
            temp_image = annotated_image.copy()
            for contour in annotations:
                points = np.array(contour, dtype=np.int32)
                cv2.polylines(temp_image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

            # Display the image with annotations
            cv2.imshow("Image Segmentation", temp_image)

            # Press 's' to save annotations, 'c' to clear, and 'q' to quit current image
            key = cv2.waitKey(1) & 0xFF
            if key == ord("s"):
                # Save annotations
                annotation_file = os.path.splitext(image_path)[0] + "_annotations.txt"
                with open(annotation_file, "w") as f:
                    for contour in annotations:
                        f.write(str(contour) + "\n")
                print(f"Annotations saved to {annotation_file}")
            elif key == ord("c"):
                # Clear annotations
                annotations.clear()
                annotated_image = image.copy()
                print("Annotations cleared")
            elif key == ord("q"):
                # Move to the next image
                annotations.clear()  # Clear annotations for the next image
                current_image_index += 1
                break

        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    # Directory containing images
    image_dir = r"C:\Users\dolko\OneDrive\Desktop\clone\immage"
    image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]

    # Segment images
    segment_images(image_files)