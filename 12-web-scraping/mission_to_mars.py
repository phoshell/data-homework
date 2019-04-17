# THIS WAS PREVIOUSLY YOUR JUPYTER NOTEBOOK
# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import hemispheres

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # print(soup.prettify())

    # results are returned as an iterable list
    news_title = soup.find('div', class_="content_title").text.strip()
    news_p = soup.find('div', class_="rollover_description_inner").text.strip()
    
    # Lets not crash the internet
    time.sleep(1)

    # Looking for the featured space picture
    # URL of page to be scraped 
    base_url = 'https://www.jpl.nasa.gov'
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)


    # Gotta click the link where the full res img resides
    image = browser.find_link_by_partial_text('FULL IMAGE')
    image.click()

    # Lets not ring the alarms
    time.sleep(1)

    # Digging deeper to get that dang img URL 
    new_html = browser.html
    print("-"*10)
    print("Here's my new URL")
    print(new_html)
    new_parse = bs(new_html, 'html.parser')

    grab_img = new_parse.find('div', class_="fancybox-inner")

    feat_src = (grab_img.find('img')['src'])

    mars_feat_img = f'{base_url}{feat_src}'
    browser.visit(mars_feat_img)

    # Boo!
    time.sleep(1)
    # Looking for the most recent Mars weather Tweet
    # URL of page to be scraped
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    twitter_html = browser.html
    response = requests.get(twitter_url)

    #Soupify Twitter
    twitter_soup = bs(twitter_html, 'html.parser')

    tweets = twitter_soup.find('div', class_='tweet')
    print("*"*10)
    print("Here's what I'm looking for")
    print("*"*10)
    mars_weather = tweets.find('p', class_='tweet-text').text
    print(mars_weather)
    # Lets not crash the internet again
    time.sleep(1)

    # List to contain dictionary Mars image titles & image_urls
    hemisphere_images =[]

    #HEMISPHERE INFO // INNER FUNCTION
# def astro(): 
#     browser = init_browser()
#     astro_start_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

#     # Go to initial page
#     browser.visit(astro_start_url)
#     time.sleep(.05)
#     print("------\nOpening Browser\n------")
#     # List of WebDriveElements
#     astro_items = browser.find_by_css("a.itemLink h3")


#     for i in range(len(astro_items)):
#         print(f"------\nMars {i+1}\n------")
#         astro_items = browser.find_by_css("a.itemLink h3")
#         astro_items[i].click()
#         time.sleep(.5)
        
#         #From image page get URL for image.
#         li_item = browser.find_by_css("div.downloads li").first
#         to_soup = bs(li_item.html, "html.parser")
#         astro_img_url = to_soup.find('a')['href']
        
#         #From image page get Title 
#         title_item = browser.find_by_css("div.content h2").text
#         #print items
#         astro_dict = { 'title' : title_item, 'img_url': astro_img_url}
#         hemisphere_images.append(astro_dict)
#         #Go to initial page
#         browser.visit(astro_start_url)
#         time.sleep(.5)


#     print('Mars Hemisphere Results')
#     print('f {title_item} {astro_img_url}')

    # CREATING MONGO DICTIONARY DATABASE 
    # Store data in a dictionary
    mars_mongo = {
        "NASA Mars News": news_title,
        "NASA Mars Info": news_p,
        "Mars Pic": mars_feat_img,
        "Mars Weather": mars_weather,
        "Mars Hemisphere Pics" : hemisphere_images,
    }

    # Close the browser after scraping
    browser.quit()
    print("-"*20)
    print("THE RESULT!!")
    print(mars_mongo)
    # Return results
    return mars_mongo