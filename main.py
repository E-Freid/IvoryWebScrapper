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


def initialize_driver():
    try:
        driver.get("https://www.ivory.co.il/catalog.php?act=cat&id=49787")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'single-item-wrapper')))
    except ConnectionError:
        print("Program can't establish connection to the site, exiting the program")
        driver.quit()
        exit(1)


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


def get_items_info(items_urls):
    for url in items_urls:
        new_item_id = get_item_info(url)
        # get new_item_info function


def get_item_urls_from_single_page(items_url_arr, url):
    try:
        driver.get(url)
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'product-anchor')))
        items = driver.find_elements(By.CLASS_NAME, 'product-anchor')
        for item in items:
            items_url_arr.append(item.get_attribute('href'))
    except ConnectionError:
        print("failed to connect to the page")


def get_items_urls():
    pages_urls = []
    items_url = []
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pagesList')))
    pages_bar = driver.find_element(By.ID, 'pagesList')
    pages = pages_bar.find_elements(By.TAG_NAME, 'a')
    pages.pop()
    pages.pop()
    pages_urls.append(driver.current_url)
    for page in pages:
        pages_urls.append(page.get_attribute('href'))
    for url in pages_urls:
        get_item_urls_from_single_page(items_url, url)
    return items_url


if __name__ == '__main__':
    initialize_driver()
    items_url = get_items_urls()
    get_items_info(items_url)
    driver.quit()
