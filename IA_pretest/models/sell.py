from database.mongoDB import connection
from bson.objectid import ObjectId
import datetime
from .prescription import Prescription


db = connection()


class Sell:
    def __init__(self, id=None, date=None, client_id=None, prescription_ids=None):
        self.id = id                 
        self.date = datetime.strptime(date, '%Y-%m-%d') if isinstance(date, str) else date
        self.client_id = client_id
        assert isinstance(prescription_ids, list), "prescription_ids must be a list"
        self.prescription_ids = prescription_ids or []
    
    @property
    def drugs(self):
        drugs_list = []
        for prescription_id in self.prescription_ids:
            prescription_data = db.prescriptions.find_one({'_id': ObjectId(prescription_id)})
            if prescription_data is not None:
                drugs_list.append(prescription_data.get('drug_name'))
        return drugs_list

    @property
    def total(self):
        total_price = 0
        for drug in self.drugs:
            drug_data = db.drugs.find_one({'name': drug})
            if drug_data is not None:
                total_price += drug_data['sell_price']
        return round(total_price, 2)



    @staticmethod
    def from_dict(data_dict):
        return Sell(
            id = data_dict['_id'],
            date = data_dict.get('date', None),
            client_id = data_dict.get('client_id', None),
            prescription_ids = data_dict.get('prescription_ids', None)
        )

    def to_dict(self):
        data = {
            'date': self.date,
            'drugs': self.drugs,
            'client_id': self.client_id,
            'prescription_ids': self.prescription_ids,
            'total': self.total
        }
        if self.id is not None:
            data['_id'] = self.id

        return data

    def create(self):
        try:
            # Vérifiez le statut de chaque prescription associée
            for prescription_id in self.prescription_ids:
                prescription_data = db.prescriptions.find_one({'_id': ObjectId(prescription_id)})
                if prescription_data is None:
                    print(f"No prescription found with id {prescription_id}")
                    return False
                elif prescription_data['status'] == 'expired':
                    print(f"Prescription {prescription_id} is expired")
                    return False  # Retourne False si la prescription est expirée
                else:
                    # Si la prescription n'est pas expirée, incrémentez 'given_nb'
                    prescription = Prescription.from_dict(prescription_data)
                    # Mettez à jour le statut dans la base de données
                    prescription.update_status()
                    db.prescriptions.update_one(
                        {'_id': ObjectId(prescription_id)},
                        {'$inc': {'given_nb': 1}}
                    )
                    print(f"Prescription {prescription_id} updated")

            if self.total != 0:
                # Insertion du document de vente dans la base de données
                inserted_sell = db.sells.insert_one(self.to_dict())
                inserted_sell_id = str(inserted_sell.inserted_id)
                print(inserted_sell_id)

                # Mise à jour du document client pour référencer la nouvelle vente
                client_data = db.clients.find_one({'_id': ObjectId(self.client_id)})
                if client_data is None:
                    print("no client found with this id")
                    return False
                else:
                    client_data['sell_ids'].append(inserted_sell_id)
                    db.clients.update_one({'_id': ObjectId(self.client_id)}, {'$set': {'sell_ids': client_data['sell_ids']}})

                # Mise à jour de la valeur du stock de chaque médicament vendu
                for drug in self.drugs:
                    drug_data = db.drugs.find_one({'name': drug})
                    if drug_data is not None:
                        if drug_data['stock'] > 0:
                            new_stock_value = drug_data['stock'] - 1  # Changez cette ligne en conséquence si vous avez une quantité spécifiée
                            db.drugs.update_one(
                                {'name': drug},
                                {'$set': {'stock': new_stock_value}}
                            )
                        else:
                            print(f"Stock of drug {drug_data['name']} is empty")
                            return False


                return True  # Retourne True si tout a réussi
            else:
                print("Total is 0")
                return False

        except Exception as e:
            print(e)
            return False  # Retourne False si une exception se produit

    @classmethod
    def get_all_sells(cls):
        try:
            sell_dicts = list(db.sells.find())
            return [Sell.from_dict(sell_dict) for sell_dict in sell_dicts]
        except Exception as e:
            print(f"Error in get_all_sells: {e}")
            return []

    @staticmethod
    def get_sells_by_client_id(client_id):
        try:
            sell_dicts = list(db.sells.find({'client_id': client_id}))
            if sell_dicts is None:
                return None
            else:
                return [Sell.from_dict(sell_dict) for sell_dict in sell_dicts]
        except Exception as e:
            print(e)
            return []
        
    @staticmethod
    def get_sell_by_id(sell_id):
        try:
            sell_dict = db.sells.find_one({'_id': ObjectId(sell_id)})
            if sell_dict is None:
                return None
            return Sell.from_dict(sell_dict)
        
        except Exception as e:
            print(e)
            return None
    

    
