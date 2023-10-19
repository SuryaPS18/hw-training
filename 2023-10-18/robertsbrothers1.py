import requests
from parsel import Selector
import time
import csv
import pymongo
class Agentscraper:
    def __init__(self):
        self.start_url = "https://www.robertsbrothers.com/roster/Agents/0"
        self.counter = 0
        self.page=2
        self.headers={
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                }
    def start(self):
            response = self.retry_request(self.start_url)
            selector = Selector(text=response.text)
            listing_url = selector.xpath('//a[@class="site-roster-card-image-link agent"]/@href').getall()
            for relative_url in listing_url:
                absolut_url = "https://www.robertsbrothers.com/" + relative_url
                print(absolut_url)
                response = self.retry_request(absolut_url)
                product_selector = Selector(text=response.text)
                self.parse(product_selector,absolut_url)

    def retry_request(self, url, max_retries=5, retry_delay=3):
        for _ in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                if response.status_code == 200:
                    return response
            except requests.exceptions.RequestException as e:
                print(f"Failed to make a request: {str(e)}")
            print(f"Retrying request to {url}...")
            time.sleep(retry_delay)
        return None
    
    def parse(self,product_selector,absolute_url):
        
            full_name = product_selector.xpath('//*[@class="rng-agent-profile-contact-name"]/text()').get()
            full_name_parts = full_name.split()
                # Initialize first, middle, and last names with defaults
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
                description = product_selector.xpath('//div[.="More information about me."]/following-sibling::div/child::div/text()').getall()
            if not description:
                description=product_selector.xpath('//*[@class="rng-agent-profile-content"]/descendant::div[2]/text()').getall()
            languages=product_selector.xpath('//small[.="Languages Spoken"]/parent::p/text()').get()
            image_url=product_selector.xpath('//img[@class="rng-agent-profile-photo"]/@src').get()
            address=product_selector.xpath('//*[@class="rng-agent-profile-contact-address"]/strong/text()').get()
            zipcode = ''.join(filter(str.isdigit,product_selector.xpath('//*[@class="rng-agent-profile-contact-address"]/text()[2]').get()))
            office_phone_number = product_selector.xpath('//div[@id="widget-text-1-preview-5503-5528648"]/text()[last()]').get()
            if office_phone_number is not None:
                office_phone_number = ''.join(filter(str.isdigit,product_selector.xpath('//div[@id="widget-text-1-preview-5503-5528648"]/text()[last()]').get()))
            agent_phone_number=product_selector.xpath('//*[@class="rng-agent-profile-contact-phone"]/a/text()').get()
            website=product_selector.xpath('//*[@class="rng-agent-profile-contact-website"]/a/@href').get()
            social=product_selector.xpath('//*[@class="rng-agent-profile-contact-social"]/descendant::a/@href').getall()
            profile_url=absolute_url
            data ={
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
              "profile_url":profile_url
                    }
            self.save_to_mongodb_and_csv(data)
    def save_to_mongodb_and_csv(self,data):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['agent_database']
        collection = db['agents']        
        collection.insert_one(data)       
        client.close()

        # Save to CSV
        filename = "agent_data_5.csv"
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if self.counter == 0:
                writer.writeheader()
            writer.writerow(data)
        self.counter +=1
            
       
        
        
    
if __name__ == "__main__":
    scraper =Agentscraper()
    scraper.start()



    # ----------------------------------completed code ---------------------------------------------------