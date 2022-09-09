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
except:
    print("Program can't establish connection to the site, exiting the program")

try:
    items_div = driver.find_element(By.XPATH, '//*[@id="productPage"]/div[3]/div[2]/div/div[1]/div[2]')
    items = items_div.find_elements(By.CLASS_NAME, 'single-item-wrapper')
    for item in items:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable(item))  # need to fix this bug
        item.click()
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'titleProd')))
            item_name = driver.find_element(By.ID, 'titleProd').text
            print(item_name)
            item_id = driver.find_element(By.XPATH, '//*[@id="productMainBlock"]/div[1]/div[3]/span/span').text
            print(item_id)
            item_price = driver.find_element(By.ID, 'pricetotalitemjs').text
            print(item_price)
        finally:
            driver.back()
finally:
    driver.quit()
