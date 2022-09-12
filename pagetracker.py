## GOAL: Gather the top 3 posts from r/freefolk and text them to me on Monday, Tuesday, and Wednesday
## TODO change to 3 posts instead of 1
## TODO filter out promoted
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import pandas as pd
import os
import sys


now = datetime.now()
month_day_year = now.strftime("%m%d%Y") #MMDDYYYY

website = 'https://www.reddit.com/r/freefolk/top/'

path = '/Users/jawsh/Downloads/chromedriver'

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
driver.get(website)

preview_pic = driver.find_elements(by='xpath', value="//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[2]/div[1]/div[1]/div[3]/div[3]/div/div[2]/div/a/div/div/img")[0].get_attribute("src")
post_title = driver.find_element(by="xpath", value=f"//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/a").text
post_link = driver.find_element(by="xpath", value=f"//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/a").get_attribute("href")

# Finds the date and time for logging the post
date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
date, time = date_time.split(',')
time = time.strip()

# Creates the initial DataFrame
posts = pd.DataFrame({"Date": date, "Time": time, "Preview Pic": preview_pic, "Title": post_title, "Link": post_link}, index=[0])

div_counter = 3
index_counter = 1
for x in range(5):
    try:
        preview_pic = driver.find_elements(by='xpath', value=f"//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[{div_counter}]/div[1]/div[1]/div[3]/div[3]/div/div[2]/div/a/div/div/img")[0].get_attribute("src")
        # This try/except below is here to deal with if a flair is on the post. If there's no flair, it runs the first. If there is flair, it runs the second.
        # TODO Could add to log the flair? Maybe add as a data point? 
        try:
            post_title = driver.find_element(by="xpath", value=f"//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[{div_counter}]/div[1]/div[1]/div[3]/div[2]/div[1]/a").text
            post_link = driver.find_element(by="xpath", value=f"//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[{div_counter}]/div[1]/div[1]/div[3]/div[2]/div[1]/a").get_attribute("href")
        except:
            post_title = driver.find_element(by="xpath", value=f"//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[{div_counter}]/div[1]/div[1]/div[3]/div[2]/div[2]/a").text
            post_link = driver.find_element(by="xpath", value=f"//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[{div_counter}]/div[1]/div[1]/div[3]/div[2]/div[2]/a").get_attribute("href")
            print("Flair post detected!")
        posts = posts.append({"Date": date, "Time": time, "Preview Pic": preview_pic, "Title": post_title, "Link": post_link}, ignore_index=True)
    except (IndexError):
        print("Non-Image Post not logged")

    div_counter += 1
    index_counter += 1






# Setting up File path
file_name = f'freefolkposts-{month_day_year}.csv'
final_path = os.path.join('/Users/jawsh/Downloads/', file_name)
posts.to_csv(final_path)


driver.quit()