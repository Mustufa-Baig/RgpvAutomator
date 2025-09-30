import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Dependencies import site_automation
from Dependencies import constants
from Dependencies import logger
from Dependencies import grade_stats




def scan(First_eno,Last_eno,new_sess=False):
   sem=constants.Sem
   if not(new_sess):
      constants.Range[0]+=1
   else:
      constants.CsvFile=First_eno+'_'+Last_eno+'.csv'

   with open(constants.ScanLogs,'w') as file:
      content=First_eno+'\n'+Last_eno+'\n'+sem+'\n'+constants.CsvFile+'\n'+constants.GNG
      file.write(content)

   chrome_options = Options()
   chrome_options.add_argument("--headless")
   chrome_options.add_argument("--window-size=1920,1080") 

   driver = webdriver.Chrome(options=chrome_options)

   if new_sess:
      logger.log("[ New Session Started ]")
      logger.log("Loading ORC model....")

   for I in range(constants.Range[0],constants.Range[1]+1):
      next_acc= constants.Batch+ '0'*(len(First_eno)-(len(constants.Batch)+len(str(I)))) + str(I)
      #print(next_acc)
      site_automation.load_account(driver,next_acc,constants.Sem,constants.GNG)
      time.sleep(0.25)


   logger.log(" ")
   logger.log(" ")
   logger.log("[ Session Complete ]")

   grade_stats.generate_stats()
   
   with open(constants.ScanLogs,'w') as file:
      file.write(' ')

   time.sleep(5)

   driver.quit()
