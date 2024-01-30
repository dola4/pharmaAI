from database.mongoDB import connection
from bson.objectid import ObjectId

db = connection()

class Adresse:
    def __init__(self,id=None, door=None, street=None, city=None, postal_code=None, state=None, country=None, client_ids=None):
        self.id = id
        self.door = door
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.state = state
        self.country = country
        self.client_ids = client_ids if client_ids is not None else []

    
    @staticmethod
    def from_dict(data_dict):
        return Adresse(
            id = data_dict.get('_id', None),
            door = data_dict.get('door', None),
            street = data_dict.get('street', None),
            city = data_dict.get('city', None),
            postal_code = data_dict.get('postal_code', None),
            state = data_dict.get('state', None),
            country = data_dict.get('country', None),
            client_ids = data_dict.get('client_ids', None)
        )
    
    def to_dict(self):
        data = {
            'door': self.door,
            'street': self.street,
            'city': self.city,
            'postal_code': self.postal_code,
            'state': self.state,
            'country': self.country,
            'client_ids': self.client_ids
        }
        if self.id is not None:
            data['_id'] = self.id

        return data

    def create(self, client_id):
        try:
            # Recherche d'une adresse existante avec les mêmes détails
            existing_adresse = db.adresses.find_one({
                'door': self.door,
                'street': self.street,
                'city': self.city,
                'postal_code': self.postal_code,
                'state': self.state,
                'country': self.country
            })

            client_data = db.clients.find_one({'_id': ObjectId(client_id)})
            if client_data is None:
                print("no client found with this id")
                return False

            # Si l'adresse existe déjà, mettez à jour la liste des client_ids
            if existing_adresse is not None:
                client_ids_as_str = [str(client_id) for client_id in existing_adresse['client_ids']]
                if client_id not in client_ids_as_str:
                    existing_adresse['client_ids'].append(client_id)
                    db.adresses.update_one(
                        {'_id': existing_adresse['_id']},
                        {'$set': {'client_ids': existing_adresse['client_ids']}}
                    )
                # Mettez à jour la liste des adress_ids du client
                if str(existing_adresse['_id']) not in client_data['adress_ids']:
                    client_data['adress_ids'].append(str(existing_adresse['_id']))
                    db.clients.update_one({'_id': ObjectId(client_id)}, {'$set': {'adress_ids': client_data['adress_ids']}})
                print(str(existing_adresse['_id']))  # Imprime l'ID de l'adresse existante
                return True
            else:
                # Si l'adresse n'existe pas, créez une nouvelle entrée
                #self.client_ids.append(client_id)
                inserted_adresse = db.adresses.insert_one(self.to_dict())
                inserted_adresse_id = str(inserted_adresse.inserted_id)
                print(inserted_adresse_id)  # Imprime l'ID de la nouvelle adresse

                # Mettez à jour la liste des adress_ids du client
                client_data['adress_ids'].append(inserted_adresse_id)
                db.clients.update_one({'_id': ObjectId(client_id)}, {'$set': {'adress_ids': client_data['adress_ids']}})
                return True

        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_all_adresses():
        try:
            adresse_dicts = list(db.adresses.find())
            return [Adresse.from_dict(adresse_dict) for adresse_dict in adresse_dicts]
        except Exception as e:
            print(e)
            return []


    @staticmethod
    def get_adress_by_client_id(client_id):
        try:
            adresse_dicts = list(db.adresses.find({'client_ids': client_id}))
            if adresse_dicts is not None:
                return [Adresse.from_dict(adresse_dict) for adresse_dict in adresse_dicts]
            else:
                return "no adresse found with this client id"
        except Exception as e:
            print(e)
            return None
    

    def update(self, adress_id):
        try:
            existing_adress = db.adresses.find_one({'_id': ObjectId(adress_id)})
            if existing_adress is None:
                return "No such address found"
            else:
                self.client_ids = existing_adress.get('client_ids', [])
                db.adresses.update_one({'_id': ObjectId(adress_id)}, {'$set': self.to_dict()})
                return True
        except Exception as e:
            print(e)
            return False
        
    @staticmethod
    def delete(adress_id):
        try:

            adress_data = db.adresses.find_one({'_id': ObjectId(adress_id)})
            if adress_data is None:
                print("No such address found")
                return False
        
            client_ids = adress_data.get('client_ids', [])
        
            for client_id in client_ids:
                client_data = db.clients.find_one({'_id': ObjectId(client_id)})
                if client_data is not None:
                    updated_adress_ids = [id for id in client_data.get('adress_ids', []) if str(id) != str(adress_id)]
                    db.clients.update_one({'_id': ObjectId(client_id)}, {'$set': {'adress_ids': updated_adress_ids}})
        
            db.adresses.delete_one({'_id': ObjectId(adress_id)})
            return True
        except Exception as e:
            print(e)
            return False

    
        