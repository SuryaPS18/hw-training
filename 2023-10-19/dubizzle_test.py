import requests
from parsel import Selector
import time
import csv
class DubizzleQatar:
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
        
        response = self.retry_request(self.start_url)      
        selector = Selector(text=response.text)
        self.parse(selector)

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
    
    def parse(self,selector):
        listing_url = selector.xpath('//*[@class="ee2b0479"]/a/@href').getall()
        for relative_url in listing_url:
            # print(relative_url)
            absolut_url = "https://www.dubizzle.qa/" + relative_url
            print(absolut_url)
                
            response = self.retry_request(absolut_url)
            
            product_selector = Selector(text=response.text)
            product_url=response.url  
            title=product_selector.xpath('//*[@aria-label="Overview"]/descendant::h1/text()').get()   
            description=product_selector.xpath('//*[@aria-label="Description"]/descendant::span/text()').getall()
            location=product_selector.xpath('//span[@aria-label="Location"]/text()').get()
            furnished=product_selector.xpath('//span[.="Furnished"]/following-sibling::span/text()').get()
            price=product_selector.xpath('//span[.="Price"]/following-sibling::span/text()').get()
            bedroom=product_selector.xpath('//span[.="Bedrooms"]/following-sibling::span/text()').get()
            bathroom=product_selector.xpath('//span[.="Bathrooms"]/following-sibling::span/text()').get()
            currency=product_selector.xpath('//*[@class="_1075545d"]/span/text()').get()
            amenities=product_selector.xpath('//*[@class="_27f9c8ac"]/span/text()').getall()
            agent_name=product_selector.xpath('//*[@class="_6d5b4928 be13fe44"]/text()').get()
            phone_number=product_selector.xpath('//*[@aria-label="Description"]/descendant::span[2]/text()').get()
                 
            data ={
               "product_url":product_url, 
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
            filename = "dubioutput4.csv"
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
        response = self.retry_request(next_page_url)
        self.page += 1
        if response is not None:
            selector = Selector(text=response.text)
            self.parse(selector)
            

    # def get_phone_number(url):
    #     url='https://www.dubizzle.qa/api/listing/120190701/contactInfo/'
    #     headers={
    #         "Accept":"application/json",
    #         "Accept-Encoding":"gzip, deflate, br",
    #         "Accept-Language":"ar",
    #         "If-None-Match":'W/"5230ad8ab9721001736995a538b4b842"',
    #         "Referer":"https://www.dubizzle.qa/en/ad/approved-open-land-for-rent-per-sqm-2-qar-ID120190701.html",
    #         "Sec-Ch-Ua":'"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    #         "Sec-Ch-Ua-Mobile":"?0",
    #         "Sec-Ch-Ua-Platform":"Linux",
    #         "Sec-Fetch-Dest":"empty",
    #         "Sec-Fetch-Mode":"cors",
    #         "Sec-Fetch-Site":"same-origin",
    #         "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    #         "X-Requested-With":"XMLHttpRequest"
    #     }
    #     response =requests.get(url,headers=headers)
    #     print(response.status_code)
    #     print(response.reason)
    #     print(response.content)

                    
    

if __name__ == "__main__":
    scraper =DubizzleQatar()
    scraper.start()





# -----------------------------------working code --------------------------------------------------------