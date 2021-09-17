from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from urllib.error import HTTPError
import urllib.request
import os
import argparse

print("명이 제작")

parser = argparse.ArgumentParser(description="Google Image Crawling")
parser.add_argument("-s","--search",action="store")
parser.add_argument("-f","--filename",action="store")
args = parser.parse_args()

search = args.search
filename = search if args.filename is None else args.filename

if search is None:
    print("google.py -h를 통해 도움말을 열람하세요.")
    quit()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPATH
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


driver = webdriver.Edge(
    executable_path=resource_path("msedgedriver.exe"))
driver.get(f'https://www.google.co.kr/search?q={search}&tbm=isch')
driver.implicitly_wait(10)

SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    driver.implicitly_wait(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector(".mye4qd").click()
        except ElementNotInteractableException:
           break
    last_height = new_height


selem = driver.find_elements_by_css_selector('.rg_i.Q4LuWd')

if not os.path.exists("img"):
    os.mkdir("img")

for i, item in enumerate(selem):
    try:
        webdriver.ActionChains(driver=driver).move_to_element(item).click(item).perform()
        driver.implicitly_wait(2)
        img_url = driver.find_element_by_css_selector(
            '#Sva75c > div > div > div.pxAole > div.tvh9oe.BIB1wf > c-wiz > div > div.OUZ5W > div.zjoqD > div.qdnLaf.isv-id > div > a > img').get_attribute("src")
        urllib.request.urlretrieve(img_url, f"img/{filename}{i}.jpg")
        print(f"Downloaded Image {i}.")

    except NoSuchElementException as E:
        print("No Such Element :",E)
    except HTTPError as E:
        print("Http Error :",E)
    

driver.close()
