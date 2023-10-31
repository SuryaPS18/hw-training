
from settings import retry_request,URL
import pymongo
from parsel import Selector
from pipeline import connect_to_mongodb


class DubizzleQatar:
    def __init__(self):
        self.start_url = "https://www.dubizzle.qa/en/properties/properties-for-rent/"
        self.counter = 0
        self.page = 2
        self.last_page=55

    def start(self):
        response = retry_request(self.start_url)      
        selector = Selector(text=response.text)
        self.extract_listing_url(selector)

    def extract_listing_url(self, selector):
        listing_urls = selector.xpath('//*[@class="ee2b0479"]/a/@href').getall()
        for relative_url in listing_urls:
            absolute_url = "https://www.dubizzle.qa/" + relative_url
            try:
               connect_to_mongodb()[URL].insert_one({"url":absolute_url})
               print(absolute_url)
            except pymongo.errors.DuplicateKeyError:
                print(f"'{absolute_url}' is already collected")

        if self.page > self.last_page:
            print("No more pages to scrape.")
            return

        self.get_next_page()

    def get_next_page(self):
        next_page_url = f"https://www.dubizzle.qa/en/properties/properties-for-rent/?page={self.page}"
        print("--------------------------------------------------------")
        print(next_page_url)
        response = retry_request(next_page_url)
        self.page += 1
        if response is not None:
            selector = Selector(text=response.text)
            self.extract_listing_url(selector)

    

if __name__ == "__main__":
    scraper = DubizzleQatar()
    scraper.start()
