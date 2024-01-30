from pymongo import MongoClient


def connection():
    #MONGODB_URI = "mongodb+srv://matpharma:srPiwY64u8HrT1sP@cluster0.rnzfdzw.mongodb.net/?retryWrites=true&w=majority"
    MONGODB_URI = "mongodb://localhost:27017/"
    client = MongoClient(MONGODB_URI)
    db = client['pharmaai']  
    return db


