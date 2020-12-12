
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd



def initial_browser():
    
    executable_path = {"executable_path": "/Users/Nataliia/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = initial_browser()

    
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")
    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    #Assign the text to variables that you can reference later.
    latest_title = soup.find_all('div', class_="content_title")[1].text
    latest_paragraph = soup.find_all('div', class_="article_teaser_body")[0].text
    
    latest_nasa_data = {
        "latest_title": latest_title,
        "latest_paragraph": latest_paragraph
        
    }
   
    browser.quit()

   
    #return data
    return latest_nasa_data
    #return latest_title

