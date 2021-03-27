from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import time
import os
def scrape_all():
    browser=init_browser()
    news_title, news_p=scrape_Nasa_Mars_news(browser)    
    mars_dict={
    "Title":news_title,
    "Paragraph":news_p,
    "FeaturedImage": scrape_JPL_Mars_Space_images(browser),
    "MarsFacts": scrape_Mars_fact(),
    "hemispheres": scrape_Mars_hemispheres(browser)
    }
    browser.quit()
    return mars_dict
def init_browser():
    # NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

    # -------------------------------------------------------------------------------
def scrape_Nasa_Mars_news(browser):
    browser.visit('https://mars.nasa.gov/news/')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    gallery = soup.find(class_='grid_gallery')
    news_title = gallery.find(class_="content_title").text
    news_p = gallery.find(class_='article_teaser_body').text
    # browser.quit()
    return news_title, news_p
    # -------------------------------------------------------------------------------
    # MARS Images
def scrape_JPL_Mars_Space_images(browser):
    url='https://spaceimages-mars.com'
    browser.visit(url)
    elem=browser.find_by_tag('button')[1]
    elem.click()
    html=browser.html
    image_soup=BeautifulSoup(html,'html.parser')
    image_url=image_soup.find('img',class_='fancybox-image').get('src')
    featured_image_url=f'https://spaceimages-mars.com/{image_url}'
    # browser.find_by_tag('input').first.fill('Featured Mars')
    # browser.find_by_id('searchHelpers_sortBy').first.select('latestDate')
    # results = browser.find_by_id('SearchListingPageResults')
    # results.links.find_by_partial_href('images').click()
    # browser.find_by_text('Download JPG ').click
    # featured_image_url = browser.url
    return featured_image_url
    # -------------------------------------------------------------------------------
    # Mars Facts
def scrape_Mars_fact():
    df=pd.read_html('https://space-facts.com/mars/')[0]
    df.columns=['Description','Mars']
    html_table= df.to_html(index=False, classes=("table table-stripe"))
    return html_table
    # -------------------------------------------------------------------------------
def scrape_Mars_hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_images_url=[]
    links=browser.find_by_css('a.product-item img')
    for i in range(4):
        hemisphere={}
        browser.find_by_css('a.product-item img')[i].click()
        sample_elem=browser.links.find_by_text('Sample').first
        hemisphere['img_url']=sample_elem['href']
        hemisphere['title']=browser.find_by_css('h2.title').text
        # html=browser.html
        # image_soup=BeautifulSoup(html,'html.parser')
        # image=image_soup.find_all('div',class_='downloads')[0].find('a')['href']
        # title=image_soup.find_all('h2',class_='title')[0].text
        # hemisphere['title']=title
        # hemisphere['image_url']=image
        hemisphere_images_url.append(hemisphere)
        browser.back()
        # browser.quit()
    return hemisphere_images_url
    # -------------------------------------------------------------------------------
def quit_browser():
    browser.quit()