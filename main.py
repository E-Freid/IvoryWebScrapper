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
    """
    this function initializes the selenium driver
    :return: None
    """
    try:
        driver.get("https://www.ivory.co.il/catalog.php?act=cat&id=49787")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'single-item-wrapper')))
    except ConnectionError:
        print("Program can't establish connection to the site, exiting the program")
        driver.quit()
        exit(1)


def get_product_info(product_url):
    """
    this function takes a product url and prints the name, price, and id.
    :param product_url: a product's url (str)
    :return: renewed product's ID and price (tuple)
    """
    try:
        driver.get(product_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'productMainBlock')))
        product_name = driver.find_element(By.ID, 'titleProd').text
        product_id = driver.find_element(By.CLASS_NAME, 'barcode-specific-area').text
        try:
            product_price = driver.find_element(By.CLASS_NAME, 'print-no-eilat-price').text
        except:
            product_price_box = driver.find_element(By.ID, 'productInfo')
            product_price = product_price_box.find_element(By.CLASS_NAME, 'price_product_page').get_attribute(
                'data-price')
        return product_name, product_id, product_price
    except ConnectionError:
        print("failed to get item data")
        return None


def get_new_product_data(renewed_product_data):
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, 'ui-id-1')))
    search_bar = driver.find_element(By.ID, 'qSearch')
    search_results_div = driver.find_element(By.ID, 'ui-id-1')
    new_product_id = renewed_product_data[1][:-1]
    search_bar_results = []
    while True: # this waits for the js to load
        try:
            search_bar.clear()
            break
        except:
            continue
    search_bar.click()
    search_bar.send_keys(new_product_id)
    try:
        WebDriverWait(search_results_div,10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'empty')))
        WebDriverWait(search_results_div,10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, 'empty')))
    except:
        pass
    WebDriverWait(search_results_div,10).until(EC.presence_of_all_elements_located((By.TAG_NAME,'li')))
    search_bar_results = search_results_div.find_elements(By.TAG_NAME, 'li')
    if len(search_bar_results) != 4:
        return None
    else:
        new_product_url = search_bar_results[2].find_element(By.TAG_NAME,'a').get_attribute('href')
        return get_product_info(new_product_url)


def get_products_info(product_urls):
    for url in product_urls:
        renewed_product_data = get_product_info(url)
        new_product_data = get_new_product_data(renewed_product_data)
        compare_and_print(new_product_data, renewed_product_data)


def compare_and_print(new_product_data, renewed_product_data):
    if new_product_data is None:
        print("Only renewed is available, showing data:")
        for i in range(0, 3):
            print(renewed_product_data[i])
        print('________________________________________')
    else:
        new_product_price = int(new_product_data[2].replace(",",""))
        renewed_product_price = int(renewed_product_data[2].replace(",",""))
        money_difference = new_product_price - renewed_product_price
        money_difference_in_percent = money_difference * 100 / new_product_price
        print("both new and renewed are available, showing data:")
        for i in range(0, 2):
            print(new_product_data[i])
        print(f'price of new: {new_product_data[2]}, price of renewed: {renewed_product_data[2]}')
        print(f'renewed costs {money_difference} less then new. ({money_difference_in_percent}% less)')
        if money_difference_in_percent > 15:
            print("this is a good deal")
        print("_________________________________________")

def get_products_url_from_single_page(product_urls, page_url):
    """
    this function appends the urls of the products in the given page
    :param product_urls: array of products urls
    :param page_url: the page from which the products urls will be appended to the array
    :return: None
    """
    try:
        driver.get(page_url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-anchor')))
        products = driver.find_elements(By.CLASS_NAME, 'product-anchor')
        for product in products:
            product_urls.append(product.get_attribute('href'))
    except ConnectionError:
        print("failed to connect to the page")


def get_products_url():
    """
    this function gets the products urls from the ivory renewed products catalog
    :return: an array of urls, each url redirects to a renewed product
    """
    pages_urls = []
    products_url = []
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pagesList')))
    pages_bar = driver.find_element(By.ID, 'pagesList')
    pages = pages_bar.find_elements(By.TAG_NAME, 'a')
    pages.pop()  # this double pop function, removes 2 unwanted pages
    pages.pop()
    pages_urls.append(driver.current_url)
    for page in pages:
        pages_urls.append(page.get_attribute('href'))
    for url in pages_urls:
        get_products_url_from_single_page(products_url, url)
    return products_url


if __name__ == '__main__':
    initialize_driver()
    products_urls = get_products_url()
    get_products_info(products_urls)
    driver.quit()
