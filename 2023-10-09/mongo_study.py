import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["database1"]
collection = db["details"]

details = {
    "name": "rahul",
    "email": "rahul@example.com",
    "age": 30
}

result = collection.insert_one(details)
print( result.inserted_id)

documents = [
    {
    "name": "sooraj m s",
    "email": "sooraj@example.com",
    "age": 30
},
    {
    "name": "sooraj v s"  ,
    "email": "soorajms@.com",
    "age": 30
},
{
    "name": "vishnu",
    "email": "vishnu@example.com",
    "age": 10
}

]
result = collection.insert_many(documents)