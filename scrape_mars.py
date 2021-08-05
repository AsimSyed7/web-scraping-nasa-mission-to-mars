from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path)

def scrape():
    browser = init_browser()
    mars_data = {}


    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    latest_news = soup.find_all('div', class_="list_text")

    news = latest_news[0]

    news_title = news.find('div', class_="content_title").text
    news_p = news.find('div', class_="article_teaser_body").text

    news_title = str(news_title)
    news_p = str(news_p)
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p

    browser.quit()

    url = 'https://spaceimages-mars.com/#'
    browser.visit(url)


    img_html = browser.html

    soup = BeautifulSoup(img_html, 'html.parser')

    images = soup.find_all('div', class_='floating_text_area')
    for image in images:
        link = image.find("a")
        href = link['href']

    featured_image_url = ("https://spaceimages-mars.com/#" + href)

    featured_image_url = str(featured_image_url)
    mars_data["featured_image_url"] = featured_image_url

    mars_facts_url = 'https://space-facts.com/mars/'

    facts_tables = pd.read_html(mars_facts_url)
    facts_tables

    facts_df = facts_tables[0]
    facts_df.columns = ['Description', 'Value']

    facts_df.set_index('Description', inplace=True)

    html_table = facts_df.to_html()

    html_table = (html_table)
    mars_data["facts_table"] = html_table


    mars_hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemis_url)
    xpath = '//div//a[@class="itemLink product-item"]/img'

    results = browser.find_by_xpath(xpath)

    hemisphere_image_urls = []

    for i in range(len(results)):
        img = results[i]
                
        img.click()
        
        mars_usgs_html = browser.html
        soup = BeautifulSoup(mars_usgs_html, 'html.parser')
        partial_img_url = soup.find("img", class_="wide-image")["src"]
        
        img_url = 'https://astrogeology.usgs.gov/' + partial_img_url
        
        img_title = soup.find('h2', class_="title").text
        
        img_url = str(img_url)
        img_title = str(img_title)
        img_dict = {
            'img_url': img_url,
            'img_title': img_title
        }
        hemisphere_image_urls.append(img_dict)

        browser.back()
        results = browser.find_by_xpath(xpath)
        i = i + 1

    mars_data['hemisphere_image_urls'] = hemisphere_image_urls


    browser.quit()

    return mars_data
