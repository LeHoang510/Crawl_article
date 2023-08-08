from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import json
from pprint import pprint

from bs4 import BeautifulSoup

url = "https://quantrimang.com/"

driver = webdriver.Chrome("/usr/local/bin/chromedriver")


driver.get(url)

category_dict = {}
subcategory_dict = {}
# get the footer
box_id = driver.find_element(By.ID, "footer")
# get the ul of cate
# all_tag = box_id.find_element(By.CSS_SELECTOR, "")
# get the list of li cate
list_cate = box_id.find_elements(By.CSS_SELECTOR, '.navigation.clearfix > li')

# for each cate
for cate in list_cate:
    # get tag a of cate
    category_a = cate.find_element(By.TAG_NAME, 'a')
    category_link = category_a.get_attribute("href")
    category_name = category_a.get_attribute("textContent").strip()
    # get tag ul of cate
    try:
        # Try to find the <ul> element within the category <div>
        category_ul = cate.find_element(By.TAG_NAME, 'ul')
    except NoSuchElementException:
        # Handle the case where category_ul is not found
        print(f"No <ul> element found for category: {category_name}")
        continue  # Move on to the next iteration

    # get tag li
    category_li = category_ul.find_elements(By.TAG_NAME, 'li')
    # temporary cate
    temp_dict = {}

    for subcategory in category_li:
        subcategory_a = subcategory.find_element(By.TAG_NAME, 'a')
        subcategory_name = subcategory.get_attribute("textContent").strip()
        subcategory_link = subcategory_a.get_attribute('href')
        # set dict
        temp_dict[subcategory_name] = subcategory_link

    subcategory_dict[category_name] = temp_dict
    category_dict[category_name] = category_link

driver.quit()

pprint(subcategory_dict, indent=4)
pprint(category_dict, indent=4)

subcategory_path = 'category_link/subcategory_link.json'
category_path = 'category_link/category_link.json'

formatted_json = json.dumps(subcategory_dict, indent=4, ensure_ascii=False)
with open(subcategory_path, 'w', encoding='utf-8') as json_file:
    json_file.write(formatted_json)

formatted_json = json.dumps(category_dict, indent=4, ensure_ascii=False)
with open(category_path, 'w', encoding='utf-8') as json_file:
    json_file.write(formatted_json)
