
import requests
import json
url = "https://ll8iz711cs-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)&x-algolia-application-id=LL8IZ711CS&x-algolia-api-key=15cb8b0a2d2d435c6613111d860ecfc5"

headers = {
    "Accept":"application/json",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
    "Connection":"keep-alive",
    "Content-Length":"1642",
    "Content-Type":"application/x-www-form-urlencoded",
    "Host":"ll8iz711cs-dsn.algolia.net",
    "Origin":"https://www.bayut.com",
    "Referer":"https://www.bayut.com/",
    "Sec-Ch-Ua":'"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    "Sec-Ch-Ua-Mobile":"?0",
    "Sec-Ch-Ua-Platform":'"Linux"',
    "Sec-Fetch-Dest":"empty",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Site":"cross-site",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}
form_data_str = '''
{
  "requests": [
    {
      "indexName": "bayut-production-ads-city-level-score-en",
      "params": "page=0&hitsPerPage=24&query=&optionalWords=&facets=%5B%5D&maxValuesPerFacet=10&attributesToHighlight=%5B%5D&attributesToRetrieve=%5B%22agency%22%2C%22area%22%2C%22baths%22%2C%22category%22%2C%22contactName%22%2C%22externalID%22%2C%22id%22%2C%22location%22%2C%22objectID%22%2C%22phoneNumber%22%2C%22coverPhoto%22%2C%22photoCount%22%2C%22price%22%2C%22product%22%2C%22productLabel%22%2C%22purpose%22%2C%22geography%22%2C%22permitNumber%22%2C%22referenceNumber%22%2C%22rentFrequency%22%2C%22rooms%22%2C%22slug%22%2C%22slug_l1%22%2C%22slug_l2%22%2C%22slug_l3%22%2C%22title%22%2C%22title_l1%22%2C%22title_l2%22%2C%22title_l3%22%2C%22createdAt%22%2C%22updatedAt%22%2C%22ownerID%22%2C%22isVerified%22%2C%22propertyTour%22%2C%22verification%22%2C%22completionStatus%22%2C%22furnishingStatus%22%2C%22-agency.tier%22%2C%22requiresLogin%22%2C%22coverVideo%22%2C%22videoCount%22%2C%22description%22%2C%22description_l1%22%2C%22description_l2%22%2C%22description_l3%22%2C%22descriptionTranslated%22%2C%22descriptionTranslated_l1%22%2C%22descriptionTranslated_l2%22%2C%22descriptionTranslated_l3%22%2C%22floorPlanID%22%2C%22panoramaCount%22%2C%22hasMatchingFloorPlans%22%2C%22hasTransactionHistory%22%2C%22state%22%2C%22photoIDs%22%2C%22reactivatedAt%22%2C%22hidePrice%22%2C%22extraFields%22%2C%22projectNumber%22%2C%22locationPurposeTier%22%2C%22ownerAgent%22%2C%22hasEmail%22%2C%22plotArea%22%5D&filters=purpose%3A%22for-sale%22%20AND%20category.slug%3A%22residential%22%20AND%20completionStatus%3A%22under-construction%22%20AND%20product%3A%22superhot%22&numericFilters="
    }
  ]
}
'''

form_data = json.loads(form_data_str)



try:
    response = requests.post(url, headers=headers,json=form_data)
    response.raise_for_status()  
    # print(response.status_code)
    # print(response.reason)
    # print(response.text)  
    data = response.json()
    hits = data['results'][0 ]['hits']
    for hit in hits:
        
        reference_number=hit.get('referenceNumber')
        print("reference_number:",reference_number)
        id = hit.get('id')
        print("id",id)
        price=hit.get('price')
        print("price",price)
        rera_permit_number=hit.get('permitNumber')
        print("rera_permit_number",rera_permit_number)
        title=hit.get('title')
        print("title",title)
        property_type=hit.get('purpose')
        print("property_type",property_type)
        bedrooms=hit.get('rooms')
        print("bedrooms",bedrooms)
        bathrooms=hit.get('baths')
        print("bathrooms",bathrooms)
        furnished=hit.get('furnishingStatus')
        print("furnished",furnished)
        owner_agent = hit.get('ownerAgent', {})
        name = owner_agent.get('name')
        print("agent_name",name)

except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'An error occurred: {err}')

