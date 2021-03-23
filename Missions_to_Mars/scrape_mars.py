from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import time
import os
def scrape_all():
    browser=init_browser()
   news, paragraph=scrape_Nasa_Mars_news('https://mars.nasa.gov/news/',browser)
   mars_dict={
    "Title":news_title,
    "Paragraph":news_p,
    "FeaturedImage": featured_image_url,
    "MarsFacts": html_table,
    "HemisphereImages": hemisphere_images_url
}
    return my_dictionary
def init_browser():
    # NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

    # -------------------------------------------------------------------------------
def scrape_Nasa_Mars_news(url, browser):
    browser.visit(images_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    gallery = soup.find(class_='grid_gallery')
    news_title = gallery.find(class_="content_title").text
    news_p = gallery.find(class_='article_teaser_body').text
    # browser.quit()
    return news_title, news_p
    # -------------------------------------------------------------------------------
    # MARS Images
def scrape_JPL_Mars_Space_images(url):
    browser.visit(url)
    browser.find_by_tag('input').first.fill('Featured Mars')
    browser.find_by_id('searchHelpers_sortBy').first.select('latestDate')
    results = browser.find_by_id('SearchListingPageResults')
    results.links.find_by_partial_href('images').click()
    browser.find_by_text('Download JPG ').click
    featured_image_url = browser.url
    return featured_image_url
    # -------------------------------------------------------------------------------
    # Mars Facts
def scrape_Mars_fact(url):
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    df=pd.read_html('https://space-facts.com/mars/')[0]
    df.columns=['Description','Mars']
    html_table= df.to_html(index=False)
    return html_table
    # -------------------------------------------------------------------------------
def scrape_Mars_hemispheres(url):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_images_url=[]
    links=browser.find_by_css('a.product-item img')
    for i in range(4):
        hemisphere={}
        browser.find_by_css('a.product-item img')[i].click()
        html=browser.html
        image_soup=BeautifulSoup(html,'html.parser')
        image=image_soup.find_all('div',class_='downloads')[0].find('a')['href']
        title=image_soup.find_all('h2',class_='title')[0].text
        hemisphere['title']=title
        hemisphere['image_url']=image
        hemisphere_images_url.append(hemisphere)
        time.sleep(0.5)
        browser.back()
        # browser.quit()
        return hemisphere
    # -------------------------------------------------------------------------------
def quit_browser():
    browser.quit()