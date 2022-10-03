## GOAL: Gather the top 3 posts from r/freefolk and text them to me on Monday, Tuesday, and Wednesday
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import pandas as pd
import os
import sys
# Python SQL toolkit and Object Relational Mapper
from sqlalchemy import create_engine
from local_settings import postgresql as settings
from local_settings import cronitor_api_key
# import psycopg2
import cronitor

cronitor.api_key = cronitor_api_key
db_path = "/Users/jawsh/devprojects/flighttracker/"
engine = create_engine('sqlite:////Users/jawsh/devprojects/flighttracker/freefolkposts.sqlite', echo=False)

#Or, you can embed telemetry events directly in your code
monitor = cronitor.Monitor('pagetracker')

# the job has started
monitor.ping(state='run')


now = datetime.now()
month_day_year = now.strftime("%m%d%Y") #MMDDYYYY
div_counter = 2
index_counter = 1
def get_post(div_counter):
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
        return [post_link, post_title, preview_pic]
    except (TypeError, IndexError):
        print("Non-Image Post not logged")

print(div_counter)
website = 'https://www.reddit.com/r/freefolk/top/'

path = '/Users/jawsh/Downloads/chromedriver'

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
driver.get(website)

post_link, post_title, preview_pic = get_post(div_counter)


# Finds the date and time for logging the post
date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
date, time = date_time.split(',')
time = time.strip()

# Creates the initial DataFrame
posts = pd.DataFrame({"Date": date, "Time": time, "Preview Pic": preview_pic, "Title": post_title, "Link": post_link}, index=[0])
print(div_counter)

div_counter += 1

print(div_counter)

for x in range(5):
    print("starting loop")
    print(div_counter)
    div_counter += 1
    
    print(div_counter)
    index_counter += 1
    try:
        preview_pic = driver.find_elements(by='xpath', value=f"//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[{div_counter}]/div[1]/div[1]/div[3]/div[3]/div/div[2]/div/a/div/div/img")[0].get_attribute("src")
        try:
            post_title = driver.find_element(by="xpath", value=f"//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[{div_counter}]/div[1]/div[1]/div[3]/div[2]/div[1]/a").text
            post_link = driver.find_element(by="xpath", value=f"//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[{div_counter}]/div[1]/div[1]/div[3]/div[2]/div[1]/a").get_attribute("href")
        except:
            post_title = driver.find_element(by="xpath", value=f"//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[{div_counter}]/div[1]/div[1]/div[3]/div[2]/div[2]/a").text
            post_link = driver.find_element(by="xpath", value=f"//div[@class='rpBJOHq2PR60pnwJlUyP0']/div[{div_counter}]/div[1]/div[1]/div[3]/div[2]/div[2]/a").get_attribute("href")
            print("Flair post detected!")
        
    except (TypeError, IndexError):
        print("Non-Image Post not logged")
        monitor.ping(state='fail')
        continue

    posts = posts.append({"Date": date, "Time": time, "Preview Pic": preview_pic, "Title": post_title, "Link": post_link}, ignore_index=True)
    
    
print(posts)

posts = posts[['Link', 'Title', 'Preview Pic', 'Date', 'Time']]
posts.loc[:, 'texted'] = ''
posts = posts.drop_duplicates().dropna()
posts = posts.set_index("Link")
posts.to_sql('textlist', con=engine, if_exists='append')


# # # # This was the old way of exporting a csv 
# # # Setting up File path
# file_name = f'freefolkposts-{month_day_year}.csv'
# final_path = os.path.join('/Users/jawsh/Downloads/', file_name)
# posts.to_csv(final_path)

# the job has completed successfully
monitor.ping(state='complete')


# TODO put into DB
driver.quit()