from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os

print('명이 제작')


def resource_path(relative_path):
    try:
        base_path = sys._MEIPATH
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


driver = webdriver.Edge(
    executable_path=resource_path("MicrosoftWebDriver.exe"))
inp = input('크롤링 : ')
driver.get(f'https://www.google.co.kr/search?q={inp}&tbm=isch')


SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    try:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                break

        last_height = new_height
    except:
        ''

selem = driver.find_elements_by_css_selector('.rg_i.Q4LuWd')

for i in range(len(selem)):
    try:
        print(i)
        selem[i].click()
        time.sleep(2)
        img_url = driver.find_element_by_css_selector(
            '#Sva75c>div>div>div.pxAole>div.tvh9oe.BIB1wf>c-wiz>div.OUZ5W>div.zjoqD>div>div.v4dQwb>a>img').get_attribute("src")
        urllib.request.urlretrieve(img_url, f"test{i}.jpg")
    except:
        print('omg')

driver.close()
