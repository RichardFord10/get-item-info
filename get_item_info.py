from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from getpass import getpass
import pandas as pd
import sys
import csv
import os
import re

# configure webdriver & headless chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options = chrome_options, executable_path=r'C:/Users/rford/Desktop/chromedriver/chromedriver.exe')

# current day format
currentDate = datetime.today().strftime('%Y-%m-%d')

#login function
def login(user, pword = str):
    driver.get("https://######.com/manager")
    Username = driver.find_element_by_id("bvuser")
    Password = driver.find_element_by_id("bvpass")
    Login = driver.find_element_by_xpath('//*[@id="form1"]/div/div[2]/input')
    Username.send_keys(user)
    Password.send_keys(pword)
    Login.click()
    print("Logging In...")
 
   
#item ids
item_ids = [
'238632',
'238225',
'235948',
'234158',
'238130',
'237470',
'231370',
'237469',
'234720',
'238494',
'236274',
'231337',
'231370',
'236567',
'238587',

]

#Result Lists
item_results = []

#start function
def get_item_info():
    print('Gathering Item Information...')
    for item_id in item_ids:
            WebDriverWait(driver, 1)  
            #Navigate to item    
            driver.get("https://www.########.com/manager/entry.php?area=general&id={}".format(item_id))
            WebDriverWait(driver,10)
            try:
                #Click 'Yes' on 'Are you sure you want to continue' view
                driver.find_element_by_css_selector('#form1 > div > input[type=submit]:nth-child(2)').click()
                WebDriverWait(driver, 5)
            except NoSuchElementException:
                pass
            #Get Name
            name = driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[1]/td[1]/textarea').text
            #Get Quick Book Name
            qb_name = driver.find_element_by_name('items[qbname]').get_attribute('value') or " N/A"
            # Get Inventory availability
            qty_available = driver.find_element_by_xpath('/html/body/form/div/table/tbody/tr[2]/td[1]/b').text[-5:]
            #Parse qty_available to pull only integers
            available = ''.join(filter(lambda i: i.isdigit(), qty_available))
            # Get MSRP
            msrp = driver.find_element_by_name('items[retail]').get_attribute('value') or " N/A "
            # Get cost depending on what type of Element displays it
            try:
                cost = driver.find_element_by_name('items[cost]').get_attribute('value') or " N/A "
            except NoSuchElementException:
                cost = driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[4]/td[2]').text or " N/A "
            except NoSuchElementException:
                cost = driver.find_element_by_xpath('//*[@id="form1"]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[4]/td[2]/input').text or " N/A "
            #Get FSP
            fsp =  driver.find_element_by_name('items[salecost]').get_attribute('value') or " N/A "
            #Get Price
            price = driver.find_element_by_name('items[price]').get_attribute('value') or " N/A "
            # Grab list of Length Options & Set Length
            cigar_length_options = Select(driver.find_element_by_name('items[clen]'))
            length = cigar_length_options.first_selected_option.text
            # Grab list of Gauge Options & Set Gauge
            gauge_length_options = Select(driver.find_element_by_name('items[cdiam]'))
            gauge = gauge_length_options.first_selected_option.text
            # Grab list of Packaging Types & Set Type
            packaging_type_options = Select(driver.find_element_by_name('items[cpack]'))
            packaging_type = packaging_type_options.first_selected_option.text
            # Grab list of Box Count & Set Count
            stick_count_options = Select(driver.find_element_by_name('items[ccount]'))
            stick_count = stick_count_options.first_selected_option.text
            #Grab list of Availabilities & Set Availability
            availability_options = Select(driver.find_element_by_name('items[availid]'))
            availability = availability_options.first_selected_option.text
            #Add data to results list
            item_results.append([item_id, name, qb_name, available, cost, price, msrp, fsp, length, gauge, packaging_type, stick_count, availability])
            #print info gathered into Terminal
            print(item_id + " " + name + " " + qb_name + " " + available + " " +  cost + " " +  price + " " + msrp + " " + fsp + " " + length + " " + gauge + " " + packaging_type + " " + stick_count + " " + availability)
    print('Item Info Data Gathered!')
    driver.quit()
    #Write items list to csv
    with open(r'C:\Users\rford\Desktop\item_info.csv', 'w+', newline='', encoding="utf-8") as file:
            writer = csv.writer(file) 
            writer.writerows(item_results)
            print('Finished Item_Info.csv')
    #Set Columns for CSV
    df = pd.read_csv(r'C:\Users\rford\Desktop\item_info.csv', header=None, index_col=None)
    df.columns = ['ID', 'Name', 'QB Name', 'Inventory', 'Cost', 'Retail', 'MSRP', 'FSP', 'Length', 'Gauge', 'Packaging', 'Stick Count', 'Availability']
    df.to_csv(r'C:\Users\rford\Desktop\item_info.csv', index=False)


#Run
login(input("Enter Username: "), getpass("Enter Password: "))
get_item_info()
 