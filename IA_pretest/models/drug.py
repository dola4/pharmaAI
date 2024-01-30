from database.mongoDB import connection
from bson.objectid import ObjectId
import datetime

db = connection()

class Drug:
    def __init__(self, id=None, name=None, stock=None, buy_price=None, sell_price=None):
        self.id = id
        self.name = name
        self.stock = stock
        self.buy_price = buy_price
        self.sell_price = sell_price
    

    
    @staticmethod
    def from_dict(data_dict):
        return Drug(
            id = data_dict.get('_id', None),
            name = data_dict.get('name', None),
            stock = data_dict.get('stock', None),
            buy_price = data_dict.get('buy_price', None),
            sell_price = data_dict.get('sell_price', None),
        )
    
    def to_dict(self):
        data = {
            'name': self.name,
            'stock': self.stock,
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
        }
        if self.id is not None:
            data['_id'] = self.id

        return data
    
    def create(self):
        try:
            if Drug.get_drug_by_name(self.name) is None:
                inserted = db.drugs.insert_one(self.to_dict())
                print (inserted.inserted_id)
                return True
            else:
                print('drug already exists')
                return False
        except Exception as e:
            print(e)
            return False
    

    @staticmethod
    def get_all_drugs():
        try:
            drug_dicts = list(db.drugs.find())
            return [Drug.from_dict(drug_dict) for drug_dict in drug_dicts]
        except Exception as e:
            print(e)
            return []
        
    @staticmethod
    def get_drug_by_id(drug_id):
        try:
            drug_dict = db.drugs.find_one({'_id': ObjectId(drug_id)})
            if drug_dict is None:
                return None
            return Drug.from_dict(drug_dict)
        except Exception as e:
            print(e)
            return None
        
    @staticmethod
    def get_drug_by_name(drug_name):
        try:
            drug_dict = db.drugs.find_one({'name': drug_name})
            if drug_dict is None:
                return None
            return Drug.from_dict(drug_dict)
        except Exception as e:
            print(e)
            return None
        

    def update(self, drug_id):
        try:
            existing_drug = db.drugs.find_one({'_id': ObjectId(drug_id)})
            if existing_drug is None:
                return False
            else:
                db.drugs.update_one({'_id': ObjectId(drug_id)}, {'$set': self.to_dict()})
                return True
        except Exception as e:
            print(e)
            return False
        
    
    @staticmethod
    def delete(drug_id):
        try:
            db.drugs.delete_one({'_id': ObjectId(drug_id)})
            return True
        except Exception as e:
            print(e)
            return False
