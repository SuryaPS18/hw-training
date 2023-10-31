

from settings import retry_request, URL, DATA
from pipeline import connect_to_mongodb
import pymongo
from parsel import Selector
import requests
import time 
import csv

def fetch_urls():
    for doc in connect_to_mongodb()[URL].find():
        url = doc.get("url")
        parse(url)

def parse(url):
    response = retry_request(url)
    if response:
        product_selector = Selector(text=response.text)
        
        title = product_selector.xpath('//*[@aria-label="Overview"]/descendant::h1/text()').get()   
        description = product_selector.xpath('//*[@aria-label="Description"]/descendant::span/text()').getall()
        location = product_selector.xpath('//span[@aria-label="Location"]/text()').get()
        furnished = product_selector.xpath('//span[.="Furnished"]/following-sibling::span/text()').get()
        price = product_selector.xpath('//span[.="Price"]/following-sibling::span/text()').get()
        bedroom = product_selector.xpath('//span[.="Bedrooms"]/following-sibling::span/text()').get()
        bathroom = product_selector.xpath('//span[.="Bathrooms"]/following-sibling::span/text()').get()
        
        currency_text = product_selector.xpath('//*[@class="_1075545d"]/span/text()').get()
        currency = currency_text.split()[0] if currency_text else None

        amenities = product_selector.xpath('//*[@class="_27f9c8ac"]/span/text()').getall()
        agent_name = product_selector.xpath('//*[@class="_6d5b4928 be13fe44"]/text()').get()
        phone_number = product_selector.xpath('//*[@aria-label="Description"]/descendant::span[2]/text()').get()
        
        extracted_data = {
            "product_url": url, 
            "title": title,    
            "description": description,
            "location": location,
            "furnished": furnished,
            "price": price,
            "bedroom": bedroom,
            "bathroom": bathroom,
            "currency": currency,
            "amenities": amenities,
            "agent_name": agent_name,
            "phone_number": phone_number
        }

        try:
            db = connect_to_mongodb()
            db[DATA].insert_one(extracted_data)
            print(f"{response.url}")
        except pymongo.errors.DuplicateKeyError:
            print(f"{response.url} already collected")

if __name__ == "__main__":
    fetch_urls()







# # ----------------------------correct code -------------------------------------------------