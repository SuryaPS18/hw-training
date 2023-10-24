import pymongo
from parsel import Selector
import requests
import time 
import csv

def fetch_urls():
    
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['dubizzle_db']
    collection = db['product_urls']     
    cursor = collection.find({}, {"url": 1})     
    for doc in cursor:
        url = doc["url"]
        parse(url)
    
    client.close()

def parse(url):
    max_retries =3
    for _ in range(max_retries):
        try:
             
        #
            response = requests.get(url,timeout=10)
            product_selector = Selector(text=response.text)
        
            
            title=product_selector.xpath('//*[@aria-label="Overview"]/descendant::h1/text()').get()   
            description=product_selector.xpath('//*[@aria-label="Description"]/descendant::span/text()').getall()
            location=product_selector.xpath('//span[@aria-label="Location"]/text()').get()
            furnished=product_selector.xpath('//span[.="Furnished"]/following-sibling::span/text()').get()
            price=product_selector.xpath('//span[.="Price"]/following-sibling::span/text()').get()
            bedroom=product_selector.xpath('//span[.="Bedrooms"]/following-sibling::span/text()').get()
            bathroom=product_selector.xpath('//span[.="Bathrooms"]/following-sibling::span/text()').get()
            
            
            currency_text = product_selector.xpath('//*[@class="_1075545d"]/span/text()').get()
            currency = currency_text.split()[0] if currency_text else None


            amenities=product_selector.xpath('//*[@class="_27f9c8ac"]/span/text()').getall()
            agent_name=product_selector.xpath('//*[@class="_6d5b4928 be13fe44"]/text()').get()
            phone_number=product_selector.xpath('//*[@aria-label="Description"]/descendant::span[2]/text()').get()
                 
            extracted_data ={
               "product_url":url, 
               "title":title,    
              "description":description,
              "location":location,
              "furnished":furnished,
              "price":price,
              "bedroom":bedroom,
              "bathroom":bathroom,
              "currency":currency,
              "amenities":amenities,
              "agent_name":agent_name,
              "phone_number":phone_number
                    }
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            db = client['dubizzle_db']
            collection = db['property_details2']
            collection.insert_one(extracted_data)

            filename = "dubizzle_data3.csv"
            with open(filename, mode="a", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=extracted_data.keys())
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(extracted_data)
            return
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            time.sleep(5)
    print(f"Max retries exceeded for URL {url}")
        
if __name__ == "__main__":
    fetch_urls()






# ----------------------------correct code -------------------------------------------------