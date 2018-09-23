# Import Dependencies
import os
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
import requests
import time

# Initialize browser
def init_browser():
    # Connects path to chromedriver

    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=True)

# Function to scrape for all required Mars data
def scrape():
    """ Scrapes all websites for Mars data """

    # Begin dictionary to store data
    scrape_mars_dict = {}

    # Visit Nasa.gov and use BeautifulSoup to scrape latest news title and summarydescription
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    # Find latest news
    results = soup.find('div', class_='features')
    news_title = results.find('div', class_='content_title').text
    newsp = results.find('div', class_='rollover_description').text

    # Store scraped data into dictionary
    scrape_mars_dict['news_title'] = news_title
    scrape_mars_dict['newsp'] = newsp

    #CONTAINS RETWEETS!!
    # # Visit twitter and scrape latest weather report
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    twitter_response = requests.get(twitter_url)
    #twitter_soup = bs(twitter_response.text, 'lxml')

    # Find weather data
    #twitter_result = twitter_soup.find('div', class_='js-tweet-text-container')
    #mars_weather = twitter_result.find('p', class_='js-tweet-text').text

    #DOES NOT CONTAIN RETWEETS!
    twitter_soup = bs(twitter_response.text, 'html.parser')
    # First, find a tweet with the data-name `Mars Weather`
    twitter_result = twitter_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    # Next, search within the tweet for the p tag containing the tweet text
    mars_weather = twitter_result.find('p', 'tweet-text').get_text()

    # Store scraped data into dictionary
    scrape_mars_dict['mars_weather'] = mars_weather

    # Visit space-facts.com and scrape facts using Pandas read_html function
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description', inplace=True)

    # Export scraped table into an html script
    mars_facts = df.to_html()
    mars_facts.replace("\n","")
    df.to_html('mars_facts.html')

    # Store scraped data to dictionary
    scrape_mars_dict['mars_facts'] = mars_facts

    # Call on chromedriver function to use for splinter
    browser = init_browser()


    # Vist Nasa and scrape latest featured image of Mars
    nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(nasa_url)

    # Use Beautiful Soup
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, "lxml")

    # Retrieve URL
    featured_image = nasa_soup.find('div', class_='default floating_text_area ms-layer').find('footer')
    featured_image_url = 'https://www.jpl.nasa.gov'+ featured_image.find('a')['data-fancybox-href']

    # Store img_url to dictionary
    scrape_mars_dict['featured_image_url'] = featured_image_url

    # Visit astrogeology.usgs.gov and scrape img urls of Mars' hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    # Use Beautiful Soup
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'lxml')
    base_url ="https://astrogeology.usgs.gov"

    # Retrieve URLs
    image_list = hemisphere_soup.find_all('div', class_='item')

    # Container for images
    hemisphere_image_urls = []

    # Loop through list of hemispheres images
    for image in image_list:

        # Store urls and titles in dictionary
        hemisphere_dict = {}

        # Find large images
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']

        # Visit URL
        browser.visit(link)

        # Halt for time
        time.sleep(1)

        # Use Beautiful Soup
        hemisphere_html2 = browser.html
        hemisphere_soup2 = bs(hemisphere_html2, 'lxml')

        # Find the img-title
        img_title = hemisphere_soup2.find('div', class_='content').find('h2', class_='title').text

        # Update dictionary
        hemisphere_dict['title'] = img_title

        # Find image url
        img_url = hemisphere_soup2.find('div', class_='downloads').find('a')['href']

        # Update dictionary
        hemisphere_dict['url_img'] = img_url

        # Update container
        hemisphere_image_urls.append(hemisphere_dict)

    # Store img data to dictionary
    scrape_mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    # Return results
    return scrape_mars_dict

    # Notes - used Week 3 instructor 'scrape_and_render' and student 'scrape_weather' activities plus other references found on GitHub to get this code to execute properly.