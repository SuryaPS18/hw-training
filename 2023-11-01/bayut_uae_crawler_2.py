import requests
import time
from settings import URL
from pipeline import mongodb_connection
class BayutuaeScraper:
    def __init__(self):
        self.start_url = "https://ll8iz711cs-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)&x-algolia-application-id=LL8IZ711CS&x-algolia-api-key=15cb8b0a2d2d435c6613111d860ecfc5"
        self.headers = {
            "Accept": "application/json",    
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }
        self.max_pages = 20
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
                        "indexName": "bayut-production-ads-city-level-score-en",
                        "params": f"page={self.page_counter}&hitsPerPage=24&query=&optionalWords=&facets=%5B%5D&maxValuesPerFacet=10&attributesToRetrieve=%5B%22agency%22%2C%22area%22%2C%22baths%22%2C%22category%22%2C%22contactName%22%2C%22externalID%22%2C%22id%22%2C%22location%22%2C%22objectID%22%2C%22phoneNumber%22%2C%22coverPhoto%22%2C%22photoCount%22%2C%22price%22%2C%22product%22%2C%22productLabel%22%2C%22purpose%22%2C%22geography%22%2C%22permitNumber%22%2C%22referenceNumber%22%2C%22rentFrequency%22%2C%22rooms%22%2C%22slug%22%2C%22slug_l1%22%2C%22slug_l2%22%2C%22slug_l3%22%2C%22title%22%2C%22title_l1%22%2C%22title_l2%22%2C%22title_l3%22%2C%22createdAt%22%2C%22updatedAt%22%2C%22ownerID%22%2C%22isVerified%22%2C%22propertyTour%22%2C%22verification%22%2C%22completionStatus%22%2C%22furnishingStatus%22%2C%22-agency.tier%22%2C%22requiresLogin%22%2C%22coverVideo%22%2C%22videoCount%22%2C%22description%22%2C%22description_l1%22%2C%22description_l2%22%2C%22description_l3%22%2C%22descriptionTranslated%22%2C%22descriptionTranslated_l1%22%2C%22descriptionTranslated_l2%22%2C%22descriptionTranslated_l3%22%2C%22floorPlanID%22%2C%22panoramaCount%22%2C%22hasMatchingFloorPlans%22%2C%22hasTransactionHistory%22%2C%22state%22%2C%22photoIDs%22%2C%22reactivatedAt%22%2C%22hidePrice%22%2C%22extraFields%22%2C%22projectNumber%22%2C%22locationPurposeTier%22%2C%22ownerAgent%22%2C%22hasEmail%22%2C%22plotArea%22%5D&filters=purpose%3A%22for-rent%22%20AND%20rentFrequency%3A%22yearly%22%20AND%20category.slug%3A%22residential%22&numericFilters="
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
                data = response.json()
                hits = data['results'][0]['hits']
                
                for hit in hits:
                    try:  
                        external_id = hit.get('externalID')  
                        if external_id is not None:              
                            property_url=f"https://www.bayut.com/property/details-{external_id}.html"
                            api_url=f"https://www.bayut.com/api/listing/?external_id={external_id}"
                        else:
                            print(f"External ID not found for hit: {hit}") 
                        data_dict={
                            'url': property_url,
                            'api_url':api_url
                        }
                        mongodb_connection()[URL].insert_one(data_dict)
                    except Exception as hit_err:
                        print(f'An error occurred while processing a hit: {hit_err}')
                        continue       
                
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
