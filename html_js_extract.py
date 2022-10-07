import requests
import os
from selenium import webdriver
import time
from chromedriver_py import binary_path
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Prep
proj_path = os.path.dirname(os.path.realpath(__file__))+'/'


# Chrome options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')

def get_html(url=''):
    # Prepare selenium to start
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(service=Service(binary_path), chrome_options=chrome_options)
    driver.minimize_window()
    driver.get(url)
    time.sleep(1)
    html = driver.execute_script('return document.getElementsByTagName("html")[0].innerHTML')
    driver.quit()
    return str(html)

if __name__ == '__main__':
    # html = str(get_html('https://www.drivingcentre.com.sg/User/Login'))
    # with open('html.txt', 'wb') as f:
    #     f.write(html.encode())

    driver = webdriver.Chrome(proj_path+'chromedriver.exe')
    driver.get('https://www.drivingcentre.com.sg/User/Login')
    time.sleep(1)
    html = driver.execute_script('return document.getElementsByTagName("html")[0].innerHTML')
    with open('html.txt', 'wb') as f:
        f.write(html.encode())
