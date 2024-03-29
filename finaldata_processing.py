import pandas as pd
import os
import shutil
import glob

# Base directory containing the Excel files
excel_dir = "./textlines"
# Base directory where each page's image segments are stored (assumes subfolders named page_1, page_2, etc.)
image_base_dir = "./train_line_segments"
# Directories to store the output images and text files
output_images_dir = "./line_data/line_images"
output_texts_dir = "./line_data/line_texts"

# Create output directories if they don't exist
os.makedirs(output_images_dir, exist_ok=True)
os.makedirs(output_texts_dir, exist_ok=True)

# List all Excel files
excel_files = glob.glob(os.path.join(excel_dir, 'p*.xlsx'))

for excel_path in excel_files:
    # Extract page number from the Excel file name (assuming naming format 'p<number>.xlsx')
    page_number = os.path.splitext(os.path.basename(excel_path))[0][1:]
    print(f"Processing page {page_number}")
    
    # Set the correct directory for the current page's images
    images_dir = os.path.join(image_base_dir, f"page_{page_number}")
    
    # Read the Excel file
    df = pd.read_excel(excel_path)

    for index, row in df.iterrows():
        # Assuming the first column has the image names without the extension and the second column has the text
        image_name = row[0] + '.jpg'  # Append the .jpg extension
        text_content = row[1]
        
        # Define the source image path and the destination paths
        src_image_path = os.path.join(images_dir, image_name)
        dest_image_path = os.path.join(output_images_dir, f"{image_name}")  # Include page number in output name
        text_file_path = os.path.join(output_texts_dir, f"{os.path.splitext(image_name)[0]}.txt")
        
        # Check if the source image exists before attempting to copy
        if os.path.exists(src_image_path):
            # Copy the image to the new directory
            shutil.copy(src_image_path, dest_image_path)
            
            # Create a text file for each line segment
            with open(text_file_path, 'w', encoding='utf-8') as file:
                file.write(text_content)
        else:
            print(f"Image file not found: {src_image_path}")

    print(f"Completed processing for page {page_number}")

print("All pages processed.")
