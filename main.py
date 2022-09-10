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
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'single-item-wrapper')))
except ConnectionError:
    print("Program can't establish connection to the site, exiting the program")


def get_item_info(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'productMainBlock')))
        item_name = driver.find_element(By.ID, 'titleProd').text
        item_id = driver.find_element(By.CLASS_NAME, 'barcode-specific-area').text
        try:
            item_price = driver.find_element(By.CLASS_NAME, 'print-no-eilat-price').text
        except:
            item_price_box = driver.find_element(By.ID, 'productInfo')
            item_price = item_price_box.find_element(By.CLASS_NAME, 'price_product_page').get_attribute('data-price')
        print(f'{item_name}, {item_id}, {item_price}')
        return item_id[:-1]
    except ConnectionError:
        print("failed to get item data")
        return None


def get_items_info(items_url):
    for url in items_url:
        new_item_idea = get_item_info(url)
        # get new_item_info function


def get_item_urls():
    items_url = []
    items = driver.find_elements(By.CLASS_NAME, 'product-anchor')
    for item in items:
        items_url.append(item.get_attribute('href'))
    return items_url


if __name__ == '__main__':
    items_url = get_item_urls()
    get_items_info(items_url)
    driver.quit()
