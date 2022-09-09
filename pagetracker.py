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



## //div[@data-testid='post-container'] -- to find all the posts on reddit page

## driver.find_element(by="xpath", value='//div[@data-testid="post-container"]') 
## //div[@class="rpBJOHq2PR60pnwJlUyP0"]/div[2]/ -- First Div controls which post you're looking at.. aka change 2 with variable
## //div[@class="rpBJOHq2PR60pnwJlUyP0"]/div[2]/div[1]/div[1]/div[3]/div[2] -- you can get title and post link from this


# Finds the top post and sends it. TODO make into a list and then loop to gather the top 3-5 posts.
preview_pic = driver.find_element(by="xpath", value="//div[@data-testid='post-container']/div[3]/div[3]/div/div[2]/div/a/div/div/img").get_attribute("src")
post_title = driver.find_element(by="xpath", value="//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/a").text
post_link = driver.find_element(by="xpath", value="//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/a").get_attribute("href")

# Finds the date and time for logging the post
date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
date, time = date_time.split(',')
time = time.strip()

# Takes data to log in csv format
posts = pd.DataFrame({"Date": date, "Time": time, "Preview Pic": preview_pic, "Title": post_title, "Link": post_link}, index=[0])

# Setting up File path
file_name = f'freefolkposts-{month_day_year}.csv'
final_path = os.path.join('/Users/jawsh/Downloads/', file_name)
posts.to_csv(final_path)


driver.quit()