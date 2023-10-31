

def connect_to_mongodb():
    from settings import MONGO_URL,MONGO_DB,URL,DATA
    from pymongo import MongoClient

    client=MongoClient(MONGO_URL)
    db=client[MONGO_DB]
    db[DATA].create_index([("product_url")],unique=True)
    db[URL].create_index([("url")],unique=True)

    return db