import cv2
import pytesseract
from pytesseract import Output
import os
import glob  # For listing image files

# Directory containing the images
image_dir = "./train_pages"
# Directory to save the segments
output_base_dir = "./train_line_segments"

if not os.path.exists(output_base_dir):
    os.makedirs(output_base_dir)

# List all jpg images in the directory
image_paths = glob.glob(os.path.join(image_dir, "*.jpg"))

for image_path in image_paths:
    print(f"Processing {image_path}")
    image_name = os.path.basename(image_path)
    image_name_without_ext = os.path.splitext(image_name)[0]

    # Create a directory for the current image's line segments
    output_dir = os.path.join(output_base_dir, image_name_without_ext)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Use PyTesseract to detect lines
    d = pytesseract.image_to_data(thresh, output_type=Output.DICT, config='--psm 6')
    n_boxes = len(d['level'])
    segments = []  # List to hold each line segment as an image

    for i in range(n_boxes):
        if int(d['block_num'][i]) == 1 and int(d['line_num'][i]) > 0:  # Ensure we are looking at line level
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            line_segment = image[y:y+h, x:x+w]
            if line_segment.shape[0] > 30 and line_segment.shape[1] > 400:
                segments.append(line_segment)

    # Save each segment as an image with image name as prefix
    for idx, segment in enumerate(segments):
        segment_path = os.path.join(output_dir, f"{image_name_without_ext}_line_segment_{idx}.jpg")
        cv2.imwrite(segment_path, segment)

    print(f"Saved {len(segments)} segments for {image_name}")
