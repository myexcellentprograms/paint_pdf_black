import os
import random
from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageDraw
# Step 1: Convert PDF to PNG images
# Step 2: Extract text from images and paint it black
# Step 3: Identify text from PDF and get modified images
# Step 4: Return modified images
def identify_text_from_pdf(pdf_path):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
    # Step 1: Convert PDF to PNG images
    images = convert_from_path(pdf_path, poppler_path=r"C:\Users\Line\AppData\Local\Programs\Python\Python311\Lib\site-packages\poppler-23.05.0\Library\bin")

    # Step 2: Extract text from images and paint it black
    modified_images = []
    for image in images:
        text = pytesseract.image_to_string(image)
        modified_image = paint_text_black(image, text)
        modified_images.append(modified_image)

    # Step 4: Return modified images
    return modified_images

def paint_text_black(image, text):
    # Create a new image with the same dimensions as the original image
    modified_image = Image.new('RGB', image.size)
    modified_image.paste(image)

    # Convert the image to grayscale for easier manipulation
    modified_image = modified_image.convert('L')

    # Create a draw object
    draw = ImageDraw.Draw(modified_image)

    # Split the text into individual words
    words = text.split()

    # Randomly select a subset of words to paint black
    words_to_paint = random.sample(words, int(len(words) * 0.1))  # Paint 10% of words

    # Get bounding boxes for each word and paint them black
    for word in words_to_paint:
        # Use pytesseract to get the bounding box coordinates for the word
        result = pytesseract.image_to_data(modified_image, output_type=pytesseract.Output.DICT)
        word_boxes = [i for i, word_text in enumerate(result['text']) if word_text == word]
        for box_index in word_boxes:
            left = result['left'][box_index]
            top = result['top'][box_index]
            width = result['width'][box_index]
            height = result['height'][box_index]
            draw.rectangle((left, top, left + width, top + height), fill='black')

    return modified_image

# Step 1: Provide the path to your PDF file
pdf_file = str(input("输入你的路径，格式如同“F:\CS1.6\doudou\example.pdf”这样："))

# Step 3: Identify text from PDF and get modified images
modified_images = identify_text_from_pdf(pdf_file)

# Step 4: Save and display modified images
for i, image in enumerate(modified_images):
    image.save(f'modified_image_{i}.png')
    image.show()
