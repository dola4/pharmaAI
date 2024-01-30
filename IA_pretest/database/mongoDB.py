from pymongo import MongoClient


def connection():
    MONGODB_URI = "mongodb://localhost:27017/"
    client = MongoClient(MONGODB_URI)
    db = client['pharmaai']  
    return db


