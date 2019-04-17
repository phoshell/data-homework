from bs4 import BeautifulSoup as bs
import splinter
from splinter import Browser
import time
# from mission_to_mars import init_browser

# Set the executable path and initialize the chrome browser in splinter
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)

def astro(): 
    browser = init_browser()
    astro_start_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Go to initial page
    browser.visit(astro_start_url)
    time.sleep(1)
    print("------\nOpening Browser\n------")
    #List of WebDriveElements
    astro_items = browser.find_by_css("a.itemLink h3")

    # List to contain dictionary of 'title', 'image_url' values.
    hemisphere_images =[]


    for i in range(len(astro_items)):
        print(f"------\nMars {i+1}\n------")
        astro_items = browser.find_by_css("a.itemLink h3")
        astro_items[i].click()
        time.sleep(1)
        
        #From image page get URL for image.
        li_item = browser.find_by_css("div.downloads li").first
        to_soup = bs(li_item.html, "html.parser")
        astro_img_url = to_soup.find('a')['href']
        
        #From image page get Title 
        title_item = browser.find_by_css("div.content h2").text
        #print items
        astro_dict = { 'title' : title_item, 'img_url': astro_img_url}
        hemisphere_images.append(astro_dict)
        #Go to initial page
        browser.visit(astro_start_url)
        time.sleep(1)


    print('Mars Hemisphere Results')
    print('f {title_item} {astro_img_url}')
