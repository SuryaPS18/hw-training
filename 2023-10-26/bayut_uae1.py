import requests
import json
import csv

url = "https://ll8iz711cs-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)&x-algolia-application-id=LL8IZ711CS&x-algolia-api-key=15cb8b0a2d2d435c6613111d860ecfc5"

headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    # Add the rest of your headers here
}
index_names =[
    "bayut-production-ads-city-level-score-en",
    "bayut-production-ads-date-desc-en"
]
common_form_data_str = '''
{
  "requests": [
    {
      "indexName": "",
      "params": "page=0&hitsPerPage=24&query=&optionalWords=&facets=%5B%5D&maxValuesPerFacet=10&attributesToHighlight=%5B%5D&attributesToRetrieve=%5B%22agency%22%2C%22area%22%2C%22baths%22%2C%22category%22%2C%22contactName%22%2C%22externalID%22%2C%22id%22%2C%22location%22%2C%22objectID%22%2C%22phoneNumber%22%2C%22coverPhoto%22%2C%22photoCount%22%2C%22price%22%2C%22product%22%2C%22productLabel%22%2C%22purpose%22%2C%22geography%22%2C%22permitNumber%22%2C%22referenceNumber%22%2C%22rentFrequency%22%2C%22rooms%22%2C%22slug%22%2C%22slug_l1%22%2C%22slug_l2%22%2C%22slug_l3%22%2C%22title%22%2C%22title_l1%22%2C%22title_l2%22%2C%22title_l3%22%2C%22createdAt%22%2C%22updatedAt%22%2C%22ownerID%22%2C%22isVerified%22%2C%22propertyTour%22%2C%22verification%22%2C%22completionStatus%22%2C%22furnishingStatus%22%2C%22-agency.tier%22%2C%22requiresLogin%22%2C%22coverVideo%22%2C%22videoCount%22%2C%22description%22%2C%22description_l1%22%2C%22description_l2%22%2C%22description_l3%22%2C%22descriptionTranslated%22%2C%22descriptionTranslated_l1%22%2C%22descriptionTranslated_l2%22%2C%22descriptionTranslated_l3%22%2C%22floorPlanID%22%2C%22panoramaCount%22%2C%22hasMatchingFloorPlans%22%2C%22hasTransactionHistory%22%2C%22state%22%2C%22photoIDs%22%2C%22reactivatedAt%22%2C%22hidePrice%22%2C%22extraFields%22%2C%22projectNumber%22%2C%22locationPurposeTier%22%2C%22ownerAgent%22%2C%22hasEmail%22%2C%22plotArea%22%5D&filters=purpose%3A%22for-sale%22%20AND%20category.slug%3A%22residential%22%20AND%20completionStatus%3A%22under-construction%22%20AND%20product%3A%22superhot%22&numericFilters="
    }
  ]
}
'''

# form_data = json.loads(form_data_str)
common_form_data = json.loads(common_form_data_str)
max_pages = 100  
filename = "bayut_uae_sample2.csv"

with open(filename, "a", newline="", encoding="utf-8") as file:
    fieldnames = ['referenceNumber', 'id', 'price', 'permitNumber', 'title', 'purpose', 'bedrooms', 'bathrooms', 'furnishingStatus', 'agent_name']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    processed_ids = set()
    for index_name in index_names:
        form_data = common_form_data.copy()
        form_data["indexName"] = index_name
      

        for page_number in range(max_pages):
            form_data['requests'][0]['params'] = form_data['requests'][0]['params'].replace('page=0', f'page={page_number}')
            print(f"Scraping page {page_number + 1}") 
            print("-----------------------------------------------------------")
            
            try:
                response = requests.post(url, headers=headers, json=form_data)
                response.raise_for_status()
                print(response.status_code)
                data = response.json()
                hits = data['results'][0]['hits']
                
                for hit in hits:
                    id = hit.get('id')
                    
                    # Check if ID has already been processed, if so, skip
                    if id in processed_ids:
                        continue                
                    processed_ids.add(id) 
                    reference_number=hit.get('referenceNumber')                
                    id = hit.get('id')                
                    price=hit.get('price')               
                    rera_permit_number=hit.get('permitNumber')                
                    title=hit.get('title')               
                    property_type=hit.get('purpose')               
                    bedrooms=hit.get('rooms')                
                    bathrooms=hit.get('baths')                
                    furnished=hit.get('furnishingStatus')                
                    owner_agent = hit.get('ownerAgent', {})
                    name = owner_agent.get('name')
                    writer.writerow({
                        'referenceNumber': reference_number,
                        'id': id,
                        'price': price,
                        'permitNumber': rera_permit_number,
                        'title': title,
                        'purpose': property_type,
                        'bedrooms': bedrooms,
                        'bathrooms': bathrooms,
                        'furnishingStatus': furnished,
                        'agent_name': name
                    })
                     
                       
            except requests.exceptions.HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                print(f'An error occurred: {err}')
    
    
