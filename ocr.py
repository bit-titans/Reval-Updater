import pytesseract
from PIL import Image, ImageEnhance, ImageColor

"""
                                            Created by ABHISHEK KOUSHIK B N
                                                        AND
                                                       AKASH R
                                            on 01/02/2019
 """



def get_ocr(src):
   # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" # Specify path to tesseract.exe from Tessaract installation
    image = Image.open(src)
    # image.show()
    (left, upper, right, lower) = (52,9,150,29)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(2.5)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.3)
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(0)
    # image = ImageColor.getcolor()
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(10.5)
    # image = image.crop((left,upper,right,lower))
    # image.show()
    text = pytesseract.image_to_string(image)
    # print("Hello")
    # print(text)
    return text