from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pprint import pprint
import time
import pandas as pd
import json

class Article:
    def __init__(self, title, link, name, date, desc, cate):
        self.title = title
        self.link = link
        self.user_name = name
        self.date = date
        self.desc = desc
        self.category = cate

# Read the JSON file and convert to a dictionary
file_path = 'category_link/subcategory_link.json'
with open(file_path, 'r', encoding='utf-8') as json_file:
    subcategory_dict = json.load(json_file)

driver = webdriver.Chrome("/usr/local/bin/chromedriver")

for category, subcategories in subcategory_dict.items():
    article_links = []
    for subcategory, link in subcategories.items():
        for i in range(5):
            driver.get(link + "?p=" + str(i))
            time.sleep(2)
            articles_li = driver.find_elements(By.CSS_SELECTOR, ".listitem.clearfix")
            for article_li in articles_li:
                try:
                    title = article_li.find_element(By.CLASS_NAME, 'title').get_attribute("textContent").strip()
                    user_name = article_li.find_element(By.CLASS_NAME, 'user-name').get_attribute("textContent").strip()
                    description = article_li.find_element(By.CLASS_NAME, 'desc').get_attribute("textContent").strip()
                    date = article_li.find_element(By.CLASS_NAME, 'date').get_attribute("textContent").strip()
                    link = article_li.find_element(By.CLASS_NAME, 'thumb').get_attribute("href")
                    article_links.append(Article(title, link, user_name, date, description, subcategory))
                except NoSuchElementException:
                    continue  # Move on to the next iteration
    # Step 1: Convert list of objectsx to list of lists
    lst = [[x.title,
            x.link,
            x.user_name,
            x.date,
            x.desc,
            x.category] for x in article_links]
    # Step 2: Convert list of lists to CSV
    df = pd.DataFrame(lst)
    df.columns = ['title', 'link', 'user_name', 'date', 'description', 'category']
    csv_name = 'article_link/'+category+'.csv'
    df.to_csv(csv_name, index=False, header=True, encoding='utf-8-sig')
    # Get the length (number of rows) of the DataFrame
    csv_length = len(df)
    print(f"CSV file has {csv_length} rows.")


#for i in article_links:
#    pprint(vars(i))


"""
df_no_duplicates = df.drop_duplicates()
df_no_duplicates.to_csv('articles_link_drop_duplicate.csv', index=False, header=True,encoding='utf-8-sig')
# Get the length (number of rows) of the DataFrame
csv_length = len(df_no_duplicates)
print(f"CSV file has {csv_length} rows.")
"""
