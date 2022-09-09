from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "/usr/local/bin/chromedriver"
s = Service(PATH)

driver = webdriver.Chrome(service=s)

try:
    driver.get("https://www.ivory.co.il/catalog.php?act=cat&id=49787")
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'single-item-wrapper')))
except ConnectionError:
    print("Program can't establish connection to the site, exiting the program")

def get_item_info(url):
    try:
        driver.get(url)
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'productMainBlock')))
        item_name = driver.find_element(By.ID, 'titleProd').text
        item_id = driver.find_element(By.CLASS_NAME,'barcode-specific-area').text
        try:
            item_price = driver.find_element(By.CLASS_NAME,'print-no-eilat-price').text
        except:
            item_price = driver.find_element(By.CLASS_NAME, 'discount-price').text
        print(f'{item_name}, {item_id}, {item_price}')
    finally:
        driver.back()


items = driver.find_elements(By.CLASS_NAME, 'single-item-wrapper')

for item in items:
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'single-item-wrapper')))
    item_url = item.find_element(By.TAG_NAME,'a').get_attribute('href')
    get_item_info(item_url)

driver.quit()