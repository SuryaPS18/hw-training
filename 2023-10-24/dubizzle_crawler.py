import requests
from parsel import Selector
import time
import pymongo
import csv

class DubizzleQatar:
    def __init__(self):
        self.start_url = "https://www.dubizzle.qa/en/properties/properties-for-rent/"
        self.counter = 0
        self.page = 2
        self.last_page=55
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }

    def start(self):
        response = self.retry_request(self.start_url)      
        selector = Selector(text=response.text)
        self.extract_listing_url(selector)

    def extract_listing_url(self, selector):
        listing_urls = selector.xpath('//*[@class="ee2b0479"]/a/@href').getall()
        for relative_url in listing_urls:
            absolute_url = "https://www.dubizzle.qa/" + relative_url
            print(absolute_url)
            self.save_to_mongodb(absolute_url)
        if self.page > self.last_page:
            print("No more pages to scrape.")
            return

        self.get_next_page()

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

    def get_next_page(self):
        next_page_url = f"https://www.dubizzle.qa/en/properties/properties-for-rent/?page={self.page}"
        print("--------------------------------------------------------")
        print(next_page_url)
        response = self.retry_request(next_page_url)
        self.page += 1
        if response is not None:
            selector = Selector(text=response.text)
            self.extract_listing_url(selector)
    def save_to_mongodb(self,absolute_url):
        # client = pymongo.MongoClient('mongodb://localhost:27017/')
        # db = client['dubizzle_db']
        # collection = db['product_urls']

        # data = {"url": absolute_url}
        # collection.insert_one(data)
        # client.close()
        filename="dubizzle_pro_url1.csv"
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if self.counter == 0:
                writer.writerow(["URL"])
            writer.writerow([absolute_url])
            self.counter +=1
if __name__ == "__main__":
    scraper = DubizzleQatar()
    scraper.start()
