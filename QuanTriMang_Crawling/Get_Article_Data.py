from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

def save_file(folder, article_name, text):
    folder_path = os.path.splitext(os.path.basename(folder))[0]
    output_folder = os.path.join("article_data", folder_path)
    article_name = article_name.replace("/", "\\")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")
    with open(f"article_data/{folder_path}/{article_name}.txt", "w", encoding="utf-8") as text_file:
        text_file.write(text)

driver = webdriver.Chrome("/usr/local/bin/chromedriver")

csv_file = "article_link/Cuộc sống.csv"

df = pd.read_csv(csv_file)
links = df["link"].values

for link in links:
    driver.get(link)
    time.sleep(2)
    contentMain = driver.find_element(By.ID, "contentMain")
    title = contentMain.find_element(By.TAG_NAME, "h1").text
    user_name = contentMain.find_element(By.CLASS_NAME, "user-name").text
    content = contentMain.find_elements(By.TAG_NAME, "p")
    article_text = ""
    for text in content:
        article_text += text.text
        article_text += "\n"

    save_file(csv_file, title, article_text)


driver.quit()