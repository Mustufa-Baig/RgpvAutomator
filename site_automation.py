from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from Dependencies import constants
from Dependencies import result_scanner
from Dependencies import captcha_scanner
from Dependencies import logger

def enrollment_fill(driver,number):
   search_box = driver.find_element(By.ID, constants.EnoId)
   search_box.clear()
   search_box.send_keys(number)

def semester_select(driver,sem):
   dropdown_element = driver.find_element(By.ID, constants.SemId)
   select = Select(dropdown_element)
   select.select_by_value(str(sem))

def grading_system_select(driver,gng):
   if gng=='g':
      radial_element = driver.find_element(By.ID, constants.GradingId)
   else:
      radial_element = driver.find_element(By.ID, constants.NonGradingId)
   
   radial_element.click()

def fill_captcha(driver,captcha):
   captcha_box = driver.find_element(By.ID, constants.CaptchaBoxId)
   captcha_box.clear()
   if captcha:
      captcha_box.send_keys(captcha)


def captcha_cycle(driver,e_no,depth=3):

   image_element = driver.find_element(By.CSS_SELECTOR,constants.CaptchaImgAlt)

   with open(constants.CaptchaFile, "wb") as file:
       file.write(image_element.screenshot_as_png)


   captcha_text=captcha_scanner.scan_captcha()


   if not(len(captcha_text)==5):
      logger.log("model switch -> "+captcha_text)
      captcha_text_new=captcha_scanner.scan_captcha(9)


      logger.log("new -> "+captcha_text_new)
      if len(captcha_text_new)<2:
         captcha_text_new=captcha_text
         logger.log("REVERT")
      captcha_text=captcha_text_new

   if not(len(captcha_text)==5):
      captcha_text="ABCDE"
      logger.log("Captcha too hard")
   
   fill_captcha(driver,'')

   button = driver.find_element(By.ID,constants.ButtonId)
   button.click()

   fill_captcha(driver,captcha_text)
   time.sleep(1.5)

   button.click()
   time.sleep(0.1)
   button.click()


   try:
      WebDriverWait(driver, 2).until(EC.alert_is_present())
      time.sleep(1)
      alert=driver.switch_to.alert
      if 'not' in str(alert.text).lower():
         logger.log("Invalid Enrolment Number",e_no,"Doesnt Exist")
         alert.accept()

      else:
         logger.log("Failed Captcha")
         alert.accept()     
         if depth<0:
            logger.log("Out of Captcha cycles",e_no,"FAILED")
         else:
            time.sleep(1.5)

            return captcha_cycle(driver,e_no,depth-1)

   except:
      return -1

def load_account(driver,e_no,sem,gng):
   driver.get(constants.SiteUrl)

   time.sleep(0.5)
   driver.find_element(By.ID, constants.RadialId).click()

   time.sleep(0.5)
   enrollment_fill(driver,e_no)

   time.sleep(0.5)
   semester_select(driver,sem)

   time.sleep(0.2)
   grading_system_select(driver,gng)

   time.sleep(4)

   r=captcha_cycle(driver,e_no,constants.CaptchaMaxAttempts)
   if r==-1:
      result_scanner.page_to_csv(e_no,[driver.find_element(By.ID,constants.TableId).get_attribute("outerHTML")])
      logger.log("Done",e_no,"Scanned")
