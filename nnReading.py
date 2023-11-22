import os

import pytesseract
from PIL import Image
import aspose.words as aw

# функция, в которую передаётся путь до картинки, текст с которой нужно прочитать
def readFile(path):
    pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR\\tesseract.exe' # ключевая строчка, код работает с помощью библиотеки Tesseract, для работы нужно установить Tesseract

    image = Image.open(path) # открывается картинка

    try:
        text = pytesseract.image_to_string(image, lang='rus')
    except Exception as e: # если произошло исключение, возращаем False и текст ошибки
        return False, e

    image_name = path.split('/')[-1].split('.')[0] # разделенние пути до картинки по слешам, нужно чтобы получить имя файла картинки

    doc = aw.Document()

    builder = aw.DocumentBuilder(doc)

    builder.write(text)

    try:
        doc.save(f"outImgText\\{image_name}.docx") # сохранение
    except Exception as e:
        return False, e

    with open(f'outImgText/{image_name}.txt', 'w') as f:
        f.write(text)

    return True, os.path.abspath(f"outImgText\\{image_name}.docx")
