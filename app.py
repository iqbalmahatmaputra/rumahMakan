from selenium import webdriver
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient
import certifi
import requests
from pprint import pprint

password = 'iqbalmp'
cxn_str = f'mongodb://iqbalmp:{password}@ac-azgceyx-shard-00-00.ligsrx6.mongodb.net:27017,ac-azgceyx-shard-00-01.ligsrx6.mongodb.net:27017,ac-azgceyx-shard-00-02.ligsrx6.mongodb.net:27017/?ssl=true&replicaSet=atlas-144b7i-shard-0&authSource=admin&retryWrites=true&w=majority'
client = MongoClient(cxn_str, tlsCAFile=certifi.where())
db = client.dbsparta_plus_week3

driver = webdriver.Chrome('./chromedriver')

url = "https://www.yelp.com/search?cflt=restaurants&amp;find_loc=San+Francisco%2C+CA"

driver.get(url)
time.sleep(2)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
time.sleep(2)

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')
restaurants = soup.select('div[class*="arrange-unit__"]')
access_token = 'pk.eyJ1IjoibGluY3hsbiIsImEiOiJjbDluMHppMjIwMTR5NDBtejl3NjNueGdyIn0.DLAhnub2hn2okIq0gwCJEw'
long = -122.420679 ## San Francisco
lat = 37.772537 ## San Francisco
for restaurant in restaurants:
    business_name = restaurant.select_one('div[class*="businessName__"]')
    if not business_name:
        continue
    name = business_name.text
    categories_price_location = restaurant.select_one('div[class*="priceCategory__"]')
    spans = categories_price_location.select('span')
    categories = spans[0].text
    location = spans[-1].text
    geo_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?proximity={long},{lat}&access_token={access_token}"
    geo_response = requests.get(geo_url)
    geo_json = geo_response.json()
    center = geo_json['features'][0]['center']
    print(name, categories, location, center)