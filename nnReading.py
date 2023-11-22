import os

import pytesseract
from PIL import Image
import aspose.words as aw

def readFile(path):
    pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR\\tesseract.exe'

    image = Image.open(path)

    try:
        text = pytesseract.image_to_string(image, lang='rus')
    except Exception as e:
        return False, e

    image_name = path.split('/')[-1].split('.')[0]

    doc = aw.Document()

    builder = aw.DocumentBuilder(doc)

    builder.write(text)

    try:
        doc.save(f"outImgText\\{image_name}.docx")
    except Exception as e:
        return False, e

    with open(f'outImgText/{image_name}.txt', 'w') as f:
        f.write(text)

    return True, os.path.abspath(f"outImgText\\{image_name}.docx")