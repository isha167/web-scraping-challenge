from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\\Users\\arune\\Downloads\\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict={}
    ### NASA Mars News

    #define the url and browse 
   #define the url and browse 
    url_mars = 'https://redplanetscience.com/'
    browser.visit(url_mars)
    html = browser.html
    soup = bs(html, 'html.parser')
   # find and print the latest news title
    news_title = soup.find_all('div',class_ = 'content_title')[0].text

   #find and print the latest news text
    news_text = soup.find_all('div',class_ = 'article_teaser_body')[0].text
    

    ### JPL Mars Space Images - Featured Image

    url_image = 'https://spaceimages-mars.com'
    browser.visit(url_image)
    html = browser.html
    soup = bs(html,'html.parser')


    
    #scrape the website to retrieve the featured image on the site and save in a variable 
    image= soup.find('img',class_='headerimage fade-in')
    featured_image= image.attrs['src']

    #full image url 
    featured_image_url= url_image +'/'+ featured_image
    print(featured_image_url)
    

    

    ### Mars Fact

    #define the url for scraping 
    url_geo = 'https://galaxyfacts-mars.com'
    table_marsfacts = pd.read_html(url_geo)
    table_marsfacts[1]
    #putting in a dataframe
    marsfacts_df = table_marsfacts[1]
    #rendering into html string
    marsfacts_html= marsfacts_df.to_html(header=True, index=True, na_rep='NaN')
    print(marsfacts_html)

    ### Mars Hemispheres

    #scraping the mars hemisphere 
    #define the url for scraping 
    url_hem = 'https://marshemispheres.com/'
    browser.visit(url_hem)
    html = browser.html
    soup = bs(html,'html.parser')

    #define the empty lists
    hems_title = []
    hems_image = []

   #find the title
    hems_list = soup.find_all('h3')
    for hems in hems_list:
        hems_new = hems.text.strip()
        hems_title.append(hems_new)

   #find the image source
   #find the url for scraping image source page
    hems =[]
    for a in soup.find_all('a',class_="itemLink product-item", href=True):
       print ("Found the URL:", a['href'])
       hems.append(a['href'])
    
  #clean the final list for url
    hems = list(dict.fromkeys(hems))
    hems.pop(4) 

    for hem in hems:
   #scrape through the url
       browser.visit(url_hem+hem)
       html = browser.html
       soup = bs(html,'html.parser')
       image=soup.find('li').a['href']
       hems_image.append(url_hem+image)
    #fill in the final list

    hemisphere_image_urls= [{'title':hems_title[0],'image':hems_image[0]},
                 {'title':hems_title[1],'image':hems_image[1]},
                {'title':hems_title[2],'image':hems_image[2]},
                {'title':hems_title[3],'image':hems_image[3]}] 

    # Create dictionary for all info scraped from sources above
    mars_dict={
        "news_title":news_title,
        "news_text":news_text,
        "featured_image_url":featured_image_url,
        "fact_table":marsfacts_html,
        "hemisphere_images":hemisphere_image_urls
    }
    # Close the browser after scraping
    return mars_dict