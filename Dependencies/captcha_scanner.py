from PIL import Image
import pytesseract

from Dependencies import constants

pytesseract.pytesseract.tesseract_cmd = constants.TesseractPath


def scan_captcha(psm=11):
   image_path = constants.CaptchaFile
   img = Image.open(image_path)

   extracted_text = pytesseract.image_to_string(img,config="--psm "+str(psm))

   return str(extracted_text).replace('\n','').replace(' ','').upper()
