from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
try:
    import autoit
except ModuleNotFoundError:
    pass
import time
import datetime
import os
import openpyxl
import pyfiglet 

choice = None
medianame = None
docChoice = None
doc_filename = None

print("\n\nDeveloped By :")
print(pyfiglet.figlet_format("mOdEL^", font = "slant" ))

unsaved_Contacts=[]
error_contacts=[]

retry=0

path_excel_file="numbers.xlsx"
wb = openpyxl.load_workbook(path_excel_file)
sheet = wb['Sheet1']
col = sheet['A']

for cell in col:
        time.sleep(1)
        inp = '"' + str(cell.value) + '"'
        unsaved_Contacts.append(inp)
print(unsaved_Contacts)

choice = input("Would you like to send attachment(yes/no): ")
if(choice == "yes"):
        # Note the media files should be present in the Media Folder
    medianame = input("Enter the Media file name you want to send: ")
docChoice = input("Would you file to send a Document file(yes/no): ")

if(docChoice == "yes"):
        # Note the document file should be present in the Document Folder
    doc_filename = input("Enter the Document file name you want to send: ")



def send_files():
    global doc_filename
    # Attachment Drop Down Menu
    clipButton = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(3)

    # To send a Document(PDF, Word file, PPT)
    docButton = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button')
    docButton.click()
    time.sleep(3)

    docPath = os.getcwd() + "\\Documents\\" + doc_filename

    autoit.control_focus("Open", "Edit1")
    autoit.control_set_text("Open", "Edit1", (docPath))
    autoit.control_click("Open", "Button1")
    time.sleep(5)  
    whatsapp_send_button = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span')
    whatsapp_send_button.click()


def send_attachment():
    global medianame
    # Attachment Drop Down Menu
    clipButton = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(3)

    # To send Videos and Images.
    mediaButton = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button')
    mediaButton.click()
    time.sleep(3)
    image_path = os.getcwd() + "\\Media\\" + medianame
    autoit.control_focus("Open", "Edit1")
    autoit.control_set_text("Open", "Edit1", image_path)
    autoit.control_click("Open", "Button1")

    time.sleep(3)  
    whatsapp_send_button = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div/span')
    whatsapp_send_button.click()
            
try:
    driver = webdriver.Chrome("chromedriver.exe")

    def send_unsaved_contact_message():
        message = input('Enter your message : ')
        # message = "mOdEL^" #HardCode it here.
        try:
            time.sleep(8)
            input_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            for ch in message:
                if ch == "\n":
                    ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
                else:
                    input_box.send_keys(ch)
            input_box.send_keys(Keys.ENTER)
            time.sleep(5)
            driver.find_element_by_class_name("web").send_keys(Keys.ENTER)
            print("Message sent successfuly")
            return True
        except NoSuchElementException:
            print("Failed to send message no Element.")
            return False


    for i in unsaved_Contacts:
        
        link = "https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(i)
        driver.get(link)
        print("Sending message to", i)
        time.sleep(3)
        tt=send_unsaved_contact_message()
        if(tt):
            continue
        else:
            while(True):
                retry +=1
                print("Retry Attempt : "+str(retry))
                link = "https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(i)
                driver.get(link)
                print("Sending message to", i)
                ttr=send_unsaved_contact_message()
                if (ttr):
                    time.sleep(3)
                    break
                elif(retry == 3):
                    retry=0
                    error_contacts.append(i)
                    break
        time.sleep(3)
        if(choice == "yes"):
            try:
                send_attachment()
            except:
                print('Attachment not sent.')
        if(docChoice == "yes"):
            try:
                send_files()
            except:
                print('Files not sent')
                time.sleep(3)
        print("Error Contacts List : ",error_contacts)
        time.sleep(2)

except Exception as e:
    print(e)
