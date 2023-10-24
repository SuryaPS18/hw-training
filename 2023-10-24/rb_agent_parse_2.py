import pymongo
from parsel import Selector
import requests
import time 

def fetch_urls():
    
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['agent_database']
    collection = db['agents_url']     
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
        
            
            full_name = product_selector.xpath('//*[@class="rng-agent-profile-contact-name"]/text()').get()
            full_name_parts = full_name.split()
                
            first_name = ""
            middle_name = ""
            last_name = ""
            if len(full_name_parts) >= 1:
                    first_name = full_name_parts[0]
            if len(full_name_parts) >= 2:
                    middle_name = full_name_parts[1]
            if len(full_name_parts) >= 3:
                    last_name = full_name_parts[2]
            title=product_selector.xpath('//*[@class="rng-agent-profile-contact-title"]/text()').get()
            description = product_selector.xpath('//h1[.="About"]/following-sibling::div[2]/p/text()').getall()    
            if not description:
                description = product_selector.xpath('//div[@style="text-align: center;"]/span/text()').getall()
            if not description:
                description = product_selector.xpath('//div[@style="text-align: center;"]/text()').getall()
            if not description:
                description=product_selector.xpath('//*[@class="rng-agent-profile-content"]/descendant::strong/text()').getall()
            if not description:
                description=product_selector.xpath('//*[@class="rng-agent-profile-content"]/div[2]/text()').getall()
            if not description:
                description=product_selector.xpath('//*[@class="rng-agent-profile-content"]/descendant::span[2]/text()').getall()
            if not description:
                description=product_selector.xpath('//*[@class="rng-agent-profile-content"]/descendant::li/text()').getall()
            languages=product_selector.xpath('//*[@class="rng-agent-profile-languages"]/text()').getall()
            image_url=product_selector.xpath('//img[@class="rng-agent-profile-photo"]/@src').get()
            address = product_selector.xpath('normalize-space(//*[@class="rng-agent-profile-contact-address"]/strong/text())').get()
            zipcode = ''.join(filter(str.isdigit,product_selector.xpath('//*[@class="rng-agent-profile-contact-address"]/text()[2]').get()))
            office_phone_number = product_selector.xpath('//div[@id="widget-text-1-preview-5503-5528648"]/text()[last()]').get()
            if office_phone_number is not None:
                office_phone_number = ''.join(filter(str.isdigit,product_selector.xpath('//div[@id="widget-text-1-preview-5503-5528648"]/text()[last()]').get()))
            agent_phone_number=product_selector.xpath('//*[@class="rng-agent-profile-contact-phone"]/a/text()').get()
            website=product_selector.xpath('//*[@class="rng-agent-profile-contact-website"]/a/@href').get()
            social=product_selector.xpath('//*[@class="rng-agent-profile-contact-social"]/descendant::a/@href').getall()
            # profile_url=absolut_url
            extracted_data ={
               "first_name":first_name,
              "middle_name":middle_name,
              "last_name":last_name,
              "title":title,
              "description":description,
              "languages":languages,
              "image_url":image_url,
              "address":address,
              "zipcode":zipcode,
              "office_phone_number":office_phone_number,
              "agent_phone_number":agent_phone_number,
              "website":website,
              "social":social,
            #   "profile_url":profile_url
                    }
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            db = client['agent_database']
            collection = db['agents_data1']
            collection.insert_one(extracted_data)
            return
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            time.sleep(5)
    print(f"Max retries exceeded for URL {url}")
        
if __name__ == "__main__":
    fetch_urls()






# ----------------------------correct code -------------------------------------------------