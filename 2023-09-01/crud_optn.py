from pymongo import MongoClient
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["bayut_db"]
collection = db["apartment"]




data = {
    "property_id" : "new_product",

    "purpose" : "For Rent",
    

    "type" : "Apartment",

    "added_on" : "26 August 2023",

    "furnishing" : "Unfurnished",


    "price" :{
        "currency" : "AED",
        "amount" : "200,000"

    },
    "location" : "Forte 2, Forte, Downtown Dubai, Dubai"

    
}

response=collection.insert_one(dict(data))
print(response)

query = {"property_id":"new_product"}
results=collection.find(query)
for document in results:
    print(document)

# filter_query = {"property_id":"new_product"}
# update_data = {"purose":"none"}
# results=collection.update_one(filter_query,update_data)
# print("modified documents:",results.modified_count)
delete_query = {"property_id":"new_product"}
result = collection.delete_one(delete_query)
print("deleted document count:",result.deleted_count)