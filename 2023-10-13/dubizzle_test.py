import requests
from parsel import Selector

import csv
class Qatarscraper:
    def __init__(self):
        self.start_url = "https://www.dubizzle.qa/en/properties/properties-for-rent/"
        self.counter = 0
        self.page=2
        self.headers={
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
                "Upgrade-Insecure-Requests":"1",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                }

        
    def start(self):
        
        response = requests.get(self.start_url,headers=self.headers)
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
            print(absolut_url)
                
            response = requests.get(absolut_url,headers=self.headers)
            if response.status_code ==200:
                product_selector = Selector(text=response.text)
                 
                data ={
               "product_url":response.url,     
              "description":product_selector.xpath('//*[@aria-label="Description"]/descendant::span/text()').getall(),
              "furnished":product_selector.xpath('//span[.="Furnished"]/following-sibling::span/text()').get(),
              "price":product_selector.xpath('//span[.="Price"]/following-sibling::span/text()').get(),
              "bedroom":product_selector.xpath('//span[.="Bedrooms"]/following-sibling::span/text()').get(),
              "bathroom":product_selector.xpath('//span[.="Bathrooms"]/following-sibling::span/text()').get(),
              "currency":product_selector.xpath('//*[@class="_1075545d"]/span/text()').get().split()[0],
              "amenities":product_selector.xpath('//*[@class="_27f9c8ac"]/span/text()').getall(),
              "agent_name":product_selector.xpath('//*[@class="_6d5b4928 be13fe44"]/text()').get()
                    }
                filename = "output3.csv"
                with open(filename, "a", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=data.keys())
                    if self.counter == 0:
                        writer.writeheader()
                    writer.writerow(data)
                # print(filename)
                self.counter += 1
        self.get_next_page()

    def get_next_page(self):
        next_page_url = f"https://www.dubizzle.qa/en/properties/properties-for-rent/?page={self.page}"
        print("--------------------------------------------------------")
        print(next_page_url)
        response = requests.get(next_page_url, headers=self.headers)

        if response.status_code == 200:
            selector = Selector(text=response.text)
            self.parse(selector)
        self.page += 1
                    
    

if __name__ == "__main__":
    scraper =Qatarscraper()
    scraper.start()
