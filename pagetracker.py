## GOAL: Gather the top 3 posts from r/freefolk and text them to me on Monday, Tuesday, and Wednesday

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import os
import sys

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


# TODO filter out promoted
