
from settings import retry_request,URL
from parsel import Selector
from pipeline import connect_to_mongodb

class BipaWebsite:
    def __init__(self):
        self.start_url="https://www.bipa.at/sitemap_0-product.xml"

    def start(self):

        r=retry_request(self.start_url)
        print(r.status_code)
        selector=Selector(text=r.text)
        links=selector.xpath("//loc/text()").getall()
        for link in links:
            print(link)
            
            connect_to_mongodb()[URL].insert_one({"url": link})





if __name__ == "__main__":
    scraper = BipaWebsite()
    scraper.start()
