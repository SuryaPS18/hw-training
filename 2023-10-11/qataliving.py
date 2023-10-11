import requests
from parsel import Selector
# import csv

class Qatarscraper:
    def __init__(self):
        self.start_url = "https://www.qatarliving.com/properties"
        self.counter = 0
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'


    def start(self):
        headers = {'User-Agent':self.user_agent}
        response = requests.get(self.start_url,headers=headers)
        print(response.status_code)
        # print(response.reason)
        if response.status_code == 200:
            selector = Selector(text=response.text)
            self.parse(selector)

    def parse(self,selector):
        product_url = selector.xpath('//*[@class="vehicle-row"]//a[@class="vehicle-row-data"]/@href').getall()
       
        print(product_url)
        # aparment = selector.css('.vehicle-row')
        # print(aparment)
    #     for apartments in aparment:
    #         relative_url = apartments.css('.vehicle-row-image a ::attr(href)').get()
    #         full_url ="https://www.qatarliving.com/" + relative_url
            
    #         response = requests.get(full_url)
    #         if response.status_code == 200:
    #                 product_selector = Selector(text=response.text)
    #                 self.parse_property_page(product_selector, response)
            

    #     next_page_url = selector.css('[title="Next"] ::attr(href)').get()
    #     if next_page_url:
    #         next_page_url = f'https://www.bayut.com/{next_page_url}'
    #         print(next_page_url)

    #         response = requests.get(next_page_url)
    #         if response.status_code == 200:
    #             selector = Selector(text=response.text)
    #             self.parse(selector)


    # def parse_property_page(self ,selector):
    #     data ={
    #         'relative_url' : selector.xpath("//*[contains(@class,'vehicle-row-image')]")
            # 'description':selector.xpath("//*[contains(@class,'content-body mt-3')]/p[9]/strong/text()").getall(),
            # 'price':selector.xpath("//*[contains(@class,'sticky-inner')]//*[contains(@class,'d-flex flex-column align-items-center')]/span/text()").get()
        # 'property_link' : response.url,
        # 'property_id': selector.xpath("//*[contains(@class, '_033281ab')]//*[@aria-label='Reference']/text()").get(),
        # 'purpose': selector.xpath("//*[contains(@class, '_033281ab')]//*[@aria-label='Purpose']/text()").get(),
        # 'type': selector.xpath("//*[contains(@class, '_033281ab')]//*[@aria-label='Type']/text()").get(),
        # 'added_on': selector.xpath("//*[contains(@class, '_033281ab')]//*[@aria-label='Reactivated date']/text()").get(),
        # 'furnishing':  selector.xpath("//*[contains(@class, '_033281ab')]//*[@aria-label='Furnishing']/text()").get(),
        # 'price':  {
        #     'currency' : selector.xpath("//*[contains(@class, 'c4fc20ba')]//*[contains(@class, 'e63a6bfb')]/text()").get(),
        #     'amount' : selector.xpath("//*[contains(@class, 'c4fc20ba')]//*[contains(@class, '_105b8a67')]/text()").get(),
        # },
        # 'location' :  selector.xpath("//*[contains(@class, '_1f0f1758')]/text()").get(),
        # 'bed_bath_size':  {
        #     'bedrooms' : selector.xpath("//*[@aria-label='Beds']//*[contains(@class, 'fc2d1086')]/text()").get(),
        #     'bathrooms' : selector.xpath("//*[@aria-label='Baths']//*[contains(@class, 'fc2d1086')]/text()").get(),
        #     'size' : selector.xpath("//*[contains(@class, 'fc2d1086')]//span/text()").get(),
        # },
        # 'agent_name' :  selector.xpath("//*[contains(@class, '_63b62ff2')]//*[contains(@class, 'f730f8e6')]/text()").get(),
        # 'img_url' :  selector.xpath('//*[@aria-label="Property image"]//*[@class="bea951ad"]/@src').get(),
        # 'breadcrumbs': ' > '.join(selector.xpath('//*[@aria-label="Breadcrumb"]//*[contains(@class, "_327a3afc")]/text()').getall()),
        # 'amenities' : selector.xpath("//*[contains(@class, '_40544a2f')]//*[contains(@class, '_005a682a')]/text()").getall(),
        # 'description' : ', '.join([size.strip() for size in selector.xpath("//*[contains(@class, '_96aa05ec')]//*[contains(@class, '_2a806e1e')]/text()").getall()]),
        # }
        # print(data)

           
        # self.save_to_csv(data)
        # self.counter += 1
            


    # def save_to_csv(self, data):
    #     filename = "bayutoutput.csv"
    #     with open(filename, "a", newline="", encoding="utf-8") as file:
    #         writer = csv.DictWriter(file, fieldnames=data.keys())
    #         if self.counter == 0:
    #             writer.writeheader()  # Write the header only if it's the first time
    #         writer.writerow(data)
    #     # print(filename)


if __name__ == "__main__":
    scraper = Qatarscraper()
    scraper.start()