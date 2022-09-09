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
    driver.implicitly_wait(10)
except ConnectionError:
    print("Program can't establish connection to the site, exiting the program")

items = driver.find_elements(By.CLASS_NAME, 'single-item-wrapper')
for item in items:
    try:
        item_url = item.find_element(By.TAG_NAME,'a').get_attribute('href')
        driver.get(item_url)
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,'titleProd')))
        item_name = driver.find_element(By.ID, 'titleProd').text
        print(item_name)
        driver.back()
    except EC.StaleElementReferenceException:
        print("Item not found")

driver.quit()