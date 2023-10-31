import requests
import time

class BayutuaeScraper:
    def __init__(self):
        self.start_url = "https://ll8iz711cs-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)&x-algolia-application-id=LL8IZ711CS&x-algolia-api-key=15cb8b0a2d2d435c6613111d860ecfc5"
        self.headers = {
            "Accept": "application/json",    
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }
        self.max_pages = 6 
        self.page_counter = 0
        self.category = "sale"

    def get_form_data(self):
        if self.category == "sale":
            return {
                "requests": [
                    {
                        "indexName": "bayut-production-ads-city-level-score-en",
                        "params": f"page={self.page_counter}&hitsPerPage=24&filters=purpose%3A%22for-sale%22%20AND%20category.slug%3A%22residential%22%20AND%20completionStatus%3A%22under-construction%22%20AND%20product%3A%22superhot%22"
                    }
                ]
            }
        elif self.category == "rent":
            return {
                "requests": [
                    {
                        "indexName": "bayut-production-agencies-en",
                        "params": f"page={self.page_counter}&hitsPerPage=24&query=&optionalWords=&facets=%5B%5D&maxValuesPerFacet=10&attributesToHighlight=%5B%5D&attributesToRetrieve=%5B%22id%22%2C%22name%22%2C%22externalID%22%2C%22logo%22%2C%22agentsCount%22%2C%22locations%22%2C%22slug%22%2C%22stats%22%2C%22phoneNumber%22%5D&filters=product%3A%22featured%22&numericFilters=stats.adsCount%3E%3D1"
                    }
                ]
            }

    def start(self):
        while self.page_counter < self.max_pages:
            try:
                form_data = self.get_form_data()
                response = self.retry_request(self.start_url, form_data)
                response.raise_for_status()  
                print(response.status_code)
                print(form_data)
                print(f"Scraping page {self.page_counter + 1}")
                print("-----------------------------------------------------------")        
                
                self.page_counter += 1

                if self.page_counter == self.max_pages:
                    if self.category == "sale":
                        self.category = "rent"
                        self.page_counter = 0
                    elif self.category == "rent":
                        break  # If you have completed scraping for rent, you can exit the loop

            except requests.exceptions.HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                break  
            except Exception as err:
                print(f'An error occurred: {err}')
                break

    def retry_request(self, url, form_data, max_retries=5, retry_delay=3):
        for _ in range(max_retries):
            try:
                response = requests.post(url, headers=self.headers, json=form_data)
                response.raise_for_status()
                print(response)
                if response.status_code ==200:
                    return response
            except requests.exceptions.RequestException as e:
                print(f"Failed to make request:{str(e)}")
            print(f"Retrying request to {url}...")
            time.sleep(retry_delay)
        return None
    
if __name__ == "__main__":
    scraper = BayutuaeScraper()
    scraper.start()
