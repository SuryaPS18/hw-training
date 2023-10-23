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
                # product_selector = Selector(text=response.text)
                self.save_to_mongodb_and_csv(absolut_url)
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
        
    def save_to_mongodb_and_csv(self,absolut_url):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['agent_database']
        collection = db['agents_url'] 
        data={"url":absolut_url}       
        collection.insert_one(data)       
        client.close()
        
        filename = "agent_url.csv"
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if self.counter == 0:
                writer.writerow(["URL"])
            writer.writerow([absolut_url])
            self.counter +=1
    












if __name__ == "__main__":
    scraper =Agentscraper()
    scraper.start()