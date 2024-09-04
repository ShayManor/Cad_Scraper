import json

from selenium import webdriver
from bs4 import BeautifulSoup
import time

from selenium.webdriver.chrome.options import Options

cad_files = []

for i in range(58):

    # Set up Selenium WebDriver
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options)

    driver.get(url)

    items = []

    # Scroll through the page to ensure all content.json is loaded
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for the page to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Dictionary to store the name and the download page link

    # Find each tile using the class "item ng-scope"
    tiles = soup.find_all('div', class_='item ng-scope')

    # Iterate through each tile
    for tile in tiles:
        # Extract the name
        name_tag = tile.find('span', class_='name ng-binding')
        name = name_tag.text if name_tag else 'Unknown'

        # Extract the link to the CAD file page
        link_tag = tile.find('a', class_='modelLink')
        detail_url = '' + link_tag['href'] if link_tag else None

        image_tag = tile.find('img', class_='previewImage')
        image_url = image_tag['src'] if image_tag else 'Unknown'

        if detail_url:
            # Add the name and link to the dictionary
            cad_files.append(detail_url)
            # cad_files.append({
            #     'name': name,
            #     'image': image_url,
            #     'detail_url': detail_url
            # })

    # Quit the driver when done
    driver.quit()
    print(i)

    # Print out the names and download links
    # print(json.dumps(cad_files))
    # for name, link, image in cad_files.items():
    #     print(f"Name: {name}, Download Page: {link}")

print(json.dumps(cad_files))
