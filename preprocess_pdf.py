from pdf2image import convert_from_path
from PIL import Image
import os
print(os.getcwd())

def split_scanned_book_pages(pdf_path, output_folder):
    # Convert PDF to a list of images
    images = convert_from_path(pdf_path)

    for i, image in enumerate(images):
        # Calculate the width and height of an image
        width, height = image.size

        # The x-coordinate of the split is at half the width
        x_coordinate = width // 2

        # Split the image into two halves
        left_page = image.crop((0, 0, x_coordinate, height))
        right_page = image.crop((x_coordinate, 0, width, height))

        # Save each page as an image
        if i != 0:
            left_page.save(f'{output_folder}/page_{2*i+1-1}.jpg')
        right_page.save(f'{output_folder}/page_{2*i+2-1}.jpg')

# Specify the path to your PDF file and the output folder
pdf_path = './Padilla.pdf'
output_folder = './output_pages'

split_scanned_book_pages(pdf_path, output_folder)
