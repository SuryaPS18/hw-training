from settings import  URL,DATA
from pipeline import mongodb_connection
from datetime import datetime
import requests
import time
import pymongo
def fetch_urls():
    for doc in mongodb_connection()[URL].find():
        api_url = doc.get("api_url")
        parse(api_url)

def parse(api_url):
    response=make_request(api_url)
    # print(response)
    data=response.json()
    reference_number=data.get('referenceNumber')
    price=data.get('price')
    id=data.get('id')
    category=data.get('purpose')
    category_url=f'https://www.bayut.com/{category}/property/uae/'
    title=data.get('title')
    description_strong=data.get('description')
    description = description_strong.replace('<strong>', '').replace('</strong>', '')
    location_list = data.get('location')
    location = [name.get('name') for name in location_list]    
    latitude=data.get('geography')['lat'] if data.get('geography') else None
    longitude=data.get('geography')['lng'] if data.get('geography') else None
    package_type=data.get('product')
    rera_permit_number=data.get('permitNumber')
    sub_category_1 = data.get('category')[0]['name'] if data.get('category') else None
    sub_category_2 = data.get('category')[1]['name'] if data.get('category') else None
    created_at=data.get('createdAt')        
    time_stamp = datetime.utcfromtimestamp(created_at)
    published_at = time_stamp.strftime('%Y-%m-%d')
    approved_at=data.get('approvedAt')
    time_stamp1= datetime.utcfromtimestamp(approved_at)
    date=time_stamp1.strftime('%Y-%m-%d')
    bedrooms=data.get('rooms')               
    bathrooms=data.get('baths') 
    number_of_photos=data.get('photoCount')
    number=data.get('phoneNumber',{})
    phone_number=number.get('proxyMobile')
    licenses = data.get('agency')['licenses']
    ded_license = None
    rera_regis = None        
    for license in licenses:
        authority = license.get('authority')
        if authority == 'DED':
            ded_license = license.get('number')
        elif authority == 'RERA':
            rera_regis = license.get('number')        
    dtcm_license=ded_license
    agent_name = data.get('agency', {}).get('name')
    broker=data.get('contactName')
    completion_status=data.get('completionStatus')
    object_id=data.get('objectID')
    user_id=data.get('ownerID')
    price_per=data.get('rentFrequency')
    furnished=data.get('furnishingStatus')
    property_type=data.get('type')
    verified=data.get('verification')['status']
    amenities = []
    for category in data['amenities']:
        for amenity in category['amenities']:
            if amenity['value'] == 'True':
                amenities.append(amenity['text'])
    external_id = data.get('externalID')  
    if external_id is not None:              
        url=f"https://www.bayut.com/property/details-{external_id}.html"
    word=data.get('title_l2')
    currency=word.split()[-3]
    extracted_data={
        "reference_number":reference_number,
        "id":id,
        "url":url,
        "price":price,
        "category":category,
        "category_url":category_url,
        "title":title,
        "description":description,
        "location":location,
        "latitude":latitude,
        "longitude":longitude,
        "package_type":package_type,
        "rera_permit_number":rera_permit_number,
        "sub_category_1":sub_category_1,
        "sub_category_2 ":sub_category_2 ,
        "published_at":published_at,
        "date":date,
        "bedrooms":bedrooms,
        "bathrooms":bathrooms,
        "number_of_photos":number_of_photos,
        "phone_number":phone_number,
        "ded_license":ded_license,
        "rera_regis":rera_regis,
        "dtcm_license":dtcm_license,
        "agent_name":agent_name,
        "broker":broker,
        "completion_status":completion_status,
        "object_id":object_id,
        "user_id":user_id,
        "price_per":price_per,
        "furnished":furnished,
        "property_type":property_type,
        "verified":verified,
        "amenities":amenities,
        "currency":currency

    }
    try:
        db=mongodb_connection()
        db[DATA].insert_one(extracted_data)
        print(f"{response.url}")
    except pymongo.errors.DuplicateKeyError:
        print(f"{response.url} already collected")
    

    


def make_request( url, max_retries=5, retry_delay=3):
        for _ in range(max_retries):
            try:
                response = requests.get(url)
                response.raise_for_status()
                if response.status_code == 200:
                    return response
            except requests.exceptions.RequestException as e:
                print(f"Failed to make a request: {str(e)}")
            print(f"Retrying request to {url}...")
            time.sleep(retry_delay)
        return None



















if __name__ == "__main__":
    fetch_urls()