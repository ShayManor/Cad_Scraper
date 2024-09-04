import csv
import json
import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
# chrome_options.add_argument("--headless")
# # chrome_options.add_argument("user-data-dir=/Users/shay/Library/Application Support/google/chrome/")  # Path to Chrome user data directory
# chrome_options.add_argument(r"user-data-dir=/Users/shay/Library/Application\ Support/Google/Chrome/")
# chrome_options.add_argument("profile-directory=Default")  # Use the correct profile if you have multiple

USER_NAME = '100026514@mvla.net'
PASSWORD = 'aaaaaa'


def recent_downloads():
    downloads_folder = '/users/shay/downloads'
    current_time = time.time()

    recent_files = []

    for filename in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, filename)
        if os.path.isfile(file_path):
            file_creation_time = os.path.getctime(file_path)
            if (current_time - file_creation_time) <= 1200:
                recent_files.append(filename)
    return recent_files


def checkCrdownload(downloads):
    for download in downloads:
        if '.crdownload' in download:
            return True
    return False


def scrape_model_info(model_url):
    driver = webdriver.Chrome(options=chrome_options)
    predownloads = recent_downloads()
    model_info = {}

    # Load the model page
    driver.get(model_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract model name
    name_element = soup.find('h1', class_='content-title title--fluid is-3 ng-binding')
    model_info['name'] = name_element.text.strip() if name_element else 'No name found'

    # Extract model description
    description_element = soup.find('div', class_='description')
    model_info['description'] = description_element.text.strip() if description_element else 'No description found'

    categories_elements = driver.find_elements(By.XPATH,
                                               '//div[@class="item"]//span[@class="title text-bold" and contains(text(),''"Categories:")]/following-sibling::span[@class="content"]/span/a')

    # Extract the text from each category element
    categories = [category.text.strip() for category in categories_elements]
    model_info['categories'] = categories

    # Find the elements containing the tags
    tags_elements = driver.find_elements(By.XPATH,
                                         '//div[@class="item"]//span[@class="title text-bold" and contains(text(),"Tags:")]/following-sibling::span['
        '@class="content"]/span/a')

    # Extract the text from each tag element
    tags = [tag.text.strip() for tag in tags_elements]
    model_info['tags'] = tags

    # Extract pictures
    image_elements = driver.find_elements(By.CSS_SELECTOR, 'div[ng-repeat="file in files"] img.image-content.ng-scope')

    # Extract the 'src' attribute from each image element
    image_urls = [image.get_attribute('src') for image in image_elements]
    images = [item for item in image_urls if item is not None]
    print(images)
    model_info['images'] = images

    # Click the download button
    download_button = driver.find_element(By.XPATH, "//button[@ng-click='download()']")
    download_button.click()

    email_input = driver.find_element(By.CSS_SELECTOR, "input[name='member[email]']")
    email_input.send_keys(USER_NAME)

    # Find the password input field and enter the password
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='member[password]']")
    password_input.send_keys(PASSWORD)

    # Find and click the sign-in button
    sign_in_button = driver.find_element(By.ID, "signInButton")
    sign_in_button.click()
    driver.implicitly_wait(15)

    for _ in range(15):
        time.sleep(1)
        downloads = recent_downloads()
        if len(downloads) == len(predownloads) + 1:
            while checkCrdownload(downloads):
                downloads = recent_downloads()
                time.sleep(3)
            time.sleep(2)
            zip_name = set(downloads) - set(predownloads)

            model_info['zip name'] = str(zip_name).replace('.zip', '')
            driver.quit()
            return model_info

        try:
            download_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='download()']"))
            )
            download_button.click()
        except (StaleElementReferenceException) as e:
            print(f"Error clicking the download button after login: {str(e)}")

    driver.quit()
    return model_info


data = []
with open('../Data/content.json') as f:
    urls = json.load(f)


for i in range(len(urls)):
    model_details = scrape_model_info(urls[i])
    with open("../Data/data.csv", "a") as f:
        w = csv.DictWriter(f, model_details.keys())
        if not data:
            w.writeheader()
        w.writerow(model_details)
    data.append(model_details)
print(data)


# model_url = 'https://grabcad.com/library/lamborghini-aventador-lp700-1'
# model_details = scrape_model_info(model_url)
# print(model_details)
