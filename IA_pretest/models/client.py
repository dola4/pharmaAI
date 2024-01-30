from database.mongoDB import connection
from bson.objectid import ObjectId

db = connection()

class Client:
    def __init__(self, id=None, first_name=None, last_name=None, age=None, sexe=None, email=None, phone=None, adress_ids=None, prescription_ids=None, sell_ids=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sexe = sexe
        self.email = email
        self.phone = phone
        self.adress_ids = adress_ids if adress_ids is not None else []
        self.prescription_ids = prescription_ids if prescription_ids is not None else []
        self.sell_ids = sell_ids if sell_ids is not None else []  

    @staticmethod
    def from_dict(data_dict):
        return Client(
            id=data_dict.get('_id', None),
            first_name=data_dict.get('first_name', None),
            last_name=data_dict.get('last_name', None),
            age=data_dict.get('age', None),
            sexe=data_dict.get('sexe', None),
            email=data_dict.get('email', None),
            phone=data_dict.get('phone', None),
            adress_ids=data_dict.get('adress_ids', None),
            prescription_ids=data_dict.get('prescription_ids', None),
            sell_ids=data_dict.get('sell_ids', None),
        )
    
    
    def to_dict(self):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'sexe': self.sexe,
            'email': self.email,
            'phone': self.phone,
            'adress_ids': self.adress_ids,
            'prescription_ids': self.prescription_ids,
            'sell_ids': self.sell_ids,
        }
        if self.id is not None:
            data['_id'] = self.id
            
        return data


    
    def create(self):
        try:
            existing_client = Client.get_client_by_email(self.email)
            if existing_client is None:
                db.clients.insert_one(self.to_dict())
                print("Client created")
                return True
            else:
                print("Email already exists")
                return False
        except Exception as e:
            print(e)
            return False
    

    @classmethod
    def get_all_clients(cls):
        try:
            clients_dicts = list(db.clients.find({}))
            return [cls.from_dict(client_dict) for client_dict in clients_dicts]
        except Exception as e:
            print(e)
            return []
        
    
    @staticmethod
    def get_client_by_email(email):
        try:
            client_dict = db.clients.find_one({'email': email})
            if client_dict is None:
                return None
            else:
                return Client.from_dict(client_dict)
        except Exception as e:
            print(e)
            return None

    def update_client(self, client_id):
        try:
            existing_client = db.clients.find_one({"_id": ObjectId(client_id)})
            if existing_client is None:
                return False
            else:
                db.clients.update_one({"_id": ObjectId(client_id)}, {"$set": self.to_dict()})
                return True
        except Exception as e:
            print(e)
            return False


    @staticmethod
    def delete_client(cls, client_id):
        try:
            db.clients.delete_one({'_id': ObjectId(client_id)})
            return True
        except Exception as e:
            print(e)
            return False    
    