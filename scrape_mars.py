#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

#Function for browser
def initial_browser():
    
    executable_path = {"executable_path": "/Users/Nataliia/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

#Additional function for parcing through html code.
#Added as there are repeated code parts in the scrape_info function
#Arguments added: browser (taking result of "initial_browser" function) and
#url (taking different urls for visiting web-pages)

def parser(browser, url):
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    return(soup)

#Additional function for scrapping html code for Hemispheres images.
#Added as there are repeated code parts in the scrape_info function
#Arguments added: soup (taking result of "parser" function),
#url (taking different urls for visiting web-pages) and 
#list for adding images urls to assigned list.

def find_image_url(soup, url, list):
    result = soup.find_all('img', class_="wide-image")[0].attrs["src"]
    list.append(url + result)
    return(list)

#Main "scrape" function
def scrape_info():
 
    #Initializing the browser
    browser = initial_browser()

    #Scrapping data about the latest news on Mars and adding new variables for storing the results    
    url_news = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    soup = parser(browser, url_news)
    latest_title = soup.find_all('div', class_="content_title")[1].text
    latest_paragraph = soup.find_all('div', class_="article_teaser_body")[0].text
    
    #Scrapping the featured image url
    url_image_search = "https://www.jpl.nasa.gov"
    url_image = url_image_search + "/spaceimages/?search=&category=Mars"
    soup = parser(browser, url_image)
    featured_image = soup.find_all("a", id="full_image")
    featured_image_link = featured_image[0].attrs["data-fancybox-href"]
    featured_image_url = url_image_search + featured_image_link

    #Scrapping Mars facts table
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    Mars_facts = tables[0]
    #Making the table more user-friendly
    Mars_facts.rename(columns={list(Mars_facts)[0]:"Parameters",
                          list(Mars_facts)[1]:"Numbers"}, inplace=True)
    Mars_facts = Mars_facts.set_index("Parameters")
    #Creating a variable for storing the table as html string
    html_table = Mars_facts.to_html()
    
    #Scrapping Hemispheres images with the additional function
    url_astrogeology = "https://astrogeology.usgs.gov"
    list_hemispheres_img_url = []
       
    url_Cerberus = "/search/map/Mars/Viking/cerberus_enhanced"
    url_Schiaparelli = "/search/map/Mars/Viking/schiaparelli_enhanced"
    url_Syrtis_Major = "/search/map/Mars/Viking/syrtis_major_enhanced"
    url_Valles_Marineris = "/search/map/Mars/Viking/valles_marineris_enhanced"

    soup = parser(browser, url_astrogeology + url_Cerberus)
    list_hemispheres_img_url = find_image_url(soup, url_astrogeology, list_hemispheres_img_url)

    soup = parser(browser, url_astrogeology + url_Schiaparelli)
    list_hemispheres_img_url = find_image_url(soup, url_astrogeology, list_hemispheres_img_url)

    soup = parser(browser, url_astrogeology + url_Syrtis_Major)
    list_hemispheres_img_url = find_image_url(soup, url_astrogeology, list_hemispheres_img_url)

    soup = parser(browser, url_astrogeology + url_Valles_Marineris)
    list_hemispheres_img_url = find_image_url(soup, url_astrogeology, list_hemispheres_img_url)
    
    #Adding images urls as a list objects to the list of dictionaries
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": list_hemispheres_img_url[0]},
        {"title": "Schiaparelli Hemisphere", "img_url": list_hemispheres_img_url[1]},
        {"title": "Syrtis Major Hemisphere", "img_url": list_hemispheres_img_url[2]},
        {"title": "Valles Marineris Hemisphere", "img_url": list_hemispheres_img_url[3]}
    ]
    
    #Creating a dictionary for storing all the scrapped data and passing 
    #it to the Mongo DB
    mars_data ={"latest_title": latest_title,
                "latest_paragraph": latest_paragraph,
                "featured_image_url": featured_image_url,
                "facts_table": html_table,
                "Hemispheres": hemisphere_image_urls
    }
    
    browser.quit()
    #Returning the created dictionary for passing it into the Mongo DB
    return mars_data