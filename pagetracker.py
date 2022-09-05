## GOAL: Gather the top 3 posts from r/freefolk and text them to me on Monday, Tuesday, and Wednesday
## TODO filter out promoted
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import os
import sys

app_path = os.path.dirname(sys.executable)

now = datetime.now()
month_day_year = now.strftime("%m%d%Y") #MMDDYYYY

website = 'https://www.reddit.com/r/freefolk/top/'

path = '/Users/jawsh/Downloads/chromedriver'

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
driver.get(website)



## //div[@data-testid='post-container'] -- to find all the posts on reddit page

## getting closer...
## driver.find_element(by="xpath", value='//div[@data-testid="post-container"]') 

# Finds the top post and sends it. TODO make into a list and then loop to gather the top 3-5 posts.
container = driver.find_element(by="xpath", value="//div[@data-testid='post-container']/div[3]/div[3]/div/div[2]/div/a/div/div/img").get_attribute("src")

# Finds the date and time for logging the post
date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
date, time = date_time.split(',')
time = time.strip()

# Takes data to log in csv format
my_dict = {"Date": date, "Time": time, "PicLink": container.text}
posts = pd.DataFrame(my_dict)

# Setting up File path
file_name = f'freefolkposts-{month_day_year}.csv'
final_path = os.path.join(app_path, file_name)
posts.to_csv(final_path)


driver.quit()