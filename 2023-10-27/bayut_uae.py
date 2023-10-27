import requests
import json
from datetime import datetime
import csv
import pymongo

base_url = "https://ll8iz711cs-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)&x-algolia-application-id=LL8IZ711CS&x-algolia-api-key=15cb8b0a2d2d435c6613111d860ecfc5"

headers = {
    "Accept": "application/json",    
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}

# Initial form data
form_data = {
    "requests": [
        {
            "indexName": "bayut-production-ads-city-level-score-en",
            "params": "page=0&hitsPerPage=24&filters=purpose%3A%22for-sale%22%20AND%20category.slug%3A%22residential%22%20AND%20completionStatus%3A%22under-construction%22%20AND%20product%3A%22superhot%22"
        }
    ]
}

max_pages = 2084  
page_counter = 0
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bayut_uae_db"]
collection = db["property_details"]
collection.create_index([("url", pymongo.ASCENDING)], unique=True)


while page_counter < max_pages:
    try:
        response = requests.post(base_url, headers=headers, json=form_data)
        response.raise_for_status()  
        print(response.status_code)
        # print(response.url)
        # print(form_data)
        # print(response.text)
        print(f"Scraping page {page_counter + 1}")
        print("-----------------------------------------------------------")
    
        # Process the response data here
        data = response.json()
        # (Add your code to extract and process the data)
        hits = data['results'][0]['hits']
        
        for hit in hits:
            try:
                reference_number=hit.get('referenceNumber')                
                
                external_id = hit.get('externalID')
                if external_id is not None:
                    
                    property_url=f"https://www.bayut.com/property/details-{external_id}.html"
                else:
                    print(f"External ID not found for hit: {hit}")               
                price=hit.get('price')               
                rera_permit_number=hit.get('permitNumber')                
                title=hit.get('title')               
                property_type=hit.get('purpose')               
                bedrooms=hit.get('rooms')                
                bathrooms=hit.get('baths')                
                furnished=hit.get('furnishingStatus')                
                owner_agent = hit.get('ownerAgent', {})
                name = owner_agent.get('name')
                user_id=hit.get('ownerID')
                number_of_photos=hit.get('photoCount')
                number=hit.get('phoneNumber',{})
                phone_number=number.get('proxyMobile')
                created_at=hit.get('createdAt')        
                timestamp = created_at
                date = datetime.utcfromtimestamp(timestamp)
                published_at = date.strftime('%Y-%m-%d')
                location_list = hit.get('location')
                location = [name.get('name') for name in location_list]
                category_list=hit.get('category')
                category=[name.get('name') for name in category_list]
                broker_display_name = hit.get('agency', {}).get('name')
                
                # Write the data to the CSV file
                data_dict={
                    'referenceNumber': reference_number,
                    'id': external_id,
                    'url': property_url,
                    'price': price,
                    'permitNumber': rera_permit_number,
                    'title': title,
                    'property_type': property_type,
                    'bedrooms': bedrooms,
                    'bathrooms': bathrooms,
                    'furnished': furnished,
                    'agent_name': name,
                    'user_id': user_id,
                    'number_of_photos': number_of_photos,
                    'phone_number': phone_number,
                    'published_at': published_at,
                    'location': location,
                    'category': category,
                    'broker_display_name': broker_display_name
                }
                collection.insert_one(data_dict)
            except Exception as hit_err:
                print(f'An error occurred while processing a hit: {hit_err}')
                continue
        
        # Update the form data for the next page
        page_counter += 1
        form_data['requests'][0]['params'] = f'page={page_counter}&hitsPerPage=24&filters=purpose%3A%22for-sale%22%20AND%20category.slug%3A%22residential%22%20AND%20completionStatus%3A%22under-construction%22%20AND%20product%3A%22superhot%22'
        print("nextpage----------------------------------------")
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        break  # Stop if an HTTP error occurs
    except Exception as err:
        print(f'An error occurred: {err}')
        break  # Stop if any other error occur