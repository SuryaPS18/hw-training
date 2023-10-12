import requests
from parsel import Selector
import re
import csv
class Qatarscraper:
    def __init__(self):
        self.start_url = "https://www.dubizzle.qa/en/properties/properties-for-rent/"
        self.counter = 0
        self.page=2
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.next_page_url = None
    def start(self):
        headers = {'User-Agent':self.user_agent}
        response = requests.get(self.start_url,headers=headers)
        print(response.status_code)
        # print(response.text)
        # print(response.reason)
        if response.status_code == 200:
            selector = Selector(text=response.text)
            self.parse(selector)
    def parse(self,selector):
            listing_url = selector.xpath('//*[@class="ee2b0479"]/a/@href').getall()
            for relative_url in listing_url:
                # print(relative_url)
                absolut_url = "https://www.dubizzle.qa/" + relative_url
                headers = {'User-Agent':self.user_agent}
                response = requests.get(absolut_url,headers=headers)
                if response.status_code ==200:
                    product_selector = Selector(text=response.text)
                    self.parse_property(product_selector)
            
            next_page_url = f"https://www.dubizzle.qa/en/properties/properties-for-rent/?page={self.page}"
            print("--------------------------------------------------------")
            print(next_page_url)
        
            headers = {'User-Agent': self.user_agent}
            response = requests.get(next_page_url, headers=headers)
            self.page += 1
               
            if response.status_code == 200:
                selector = Selector(text=response.text)
                self.parse(selector)


    def parse_property(self,selector):
         data ={
              "description":selector.xpath('//*[@class="_0f86855a"]/span/text()').get(),
              "furnished":selector.xpath('//span[.="Furnished"]/following-sibling::span/text()').get(),
              "price":selector.xpath('//span[.="Price"]/following-sibling::span/text()').get(),
              "bedroom":selector.xpath('//span[.="Bedrooms"]/following-sibling::span/text()').get(),
              "bathroom":selector.xpath('//span[.="Bathrooms"]/following-sibling::span/text()').get(),
              "currency":selector.xpath('//*[@class="_1075545d"]/span/text()').get(),
              "amenities":selector.xpath('//*[@class="_27f9c8ac"]/span/text()').getall(),
              "agent_name":selector.xpath('//*[@class="_6d5b4928 be13fe44"]/text()').get()
         }
        #  print(data)
         if self.counter < 1000:
            self.save_to_csv(data)
            self.counter +=1
            if self.counter >= 1000:
                print("reached thevresponse limit")
    def save_to_csv(self, data):
        filename = "dubizzleoutput.csv"
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if self.counter == 0:
                writer.writeheader()
            writer.writerow(data)

if __name__ == "__main__":
    scraper =Qatarscraper()
    scraper.start()