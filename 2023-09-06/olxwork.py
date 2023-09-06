import requests
import json
from parsel import Selector

class OLXScraper:
    def __init__(self):
        self.start_url = "https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723"
        self.counter = 0
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

    def start(self):
        headers = {'User-Agent': self.user_agent}
        response = requests.get(self.start_url, headers=headers)
        print(response.status_code)
        print(response.reason)
        if response.status_code == 200:
            selector = Selector(text=response.text)
            self.parse(selector)

    def parse(self, selector):
        listing_urls = selector.xpath('//li[contains(@class, "_1DNjI")]/a/@href').getall()
        for relative_url in listing_urls:
            print(relative_url)
            absolute_url = 'https://www.olx.in' + relative_url
            headers = {'User-Agent': self.user_agent} 
            response = requests.get(absolute_url,headers=headers)
            if response.status_code == 200:
                property_selector = Selector(text=response.text)
                self.parse_property(property_selector)

            if self.counter >= 1000:
                break  # Stop when you reach 1000 listings

    def parse_property(self, selector):
        data = {
            "property_name": selector.xpath('//h1[contains(@class, "_1hJph")]/text()').get(),
            "property_id": selector.re_first(r'\d+', '//div[contains(@class, "_1-oS0")]/strong/text()'),
            "breadcrumbs": selector.xpath('//ol[contains(@class, "rui-2Pidb")]//li/a/text()').getall(),
            "price": selector.xpath('//span[contains(@class, "T8y-z")]/text()').re_first(r'\d+'),
            "image_url": selector.xpath('//div[@class="_23Jeb"]/figure/img/@src').get(),
            "description": selector.xpath('//div[@data-aut-id="itemDescriptionContent"]/p/text()').get(),
            "seller_name": selector.xpath('//div[contains(@class, "eHFQs")]/text()').get(),
            "location": selector.xpath('//span[contains(@class, "_1RkZP")]/text()').get(),
            "property_type": selector.xpath('//span[contains(@class, "B6X7c")]/text()').get(),
            "bathrooms": selector.xpath('//span[@data-aut-id="value_bathrooms"]/text()').get(),
            "bedrooms": selector.xpath('//span[@data-aut-id="value_rooms"]/text()').get()
        }

        self.save_to_json(data)

    def save_to_json(self, data):
        filename = 'output.json'
        with open(filename, 'a') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.write('\n')

if __name__ == '__main__':
    scraper = OLXScraper()
    scraper.start()