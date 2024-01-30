from database.mongoDB import connection
from bson.objectid import ObjectId
from datetime import datetime

db = connection()

class Prescription:
    def __init__(self, id=None, client_id=None, given_date=None, expiration_date=None, drug_name=None, hospital=None, doctor=None, max_given=None, given_nb=0):
        self.id = id
        self.client_id = client_id
        self.given_date = datetime.strptime(given_date, '%Y-%m-%d') if isinstance(given_date, str) else given_date
        self.expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d') if isinstance(expiration_date, str) else expiration_date
        self.drug_name = drug_name
        self.hospital = hospital
        self.doctor = doctor
        self.max_given = max_given
        self.given_nb = given_nb
    
        
    @property 
    def status(self):
        today = datetime.today().date()  # Convertit datetime.datetime à datetime.date
        expiration_date = self.expiration_date.date() if isinstance(self.expiration_date, datetime) else self.expiration_date
        if expiration_date >= today and self.given_nb < self.max_given:
            return 'active'
        else:
            return 'expired'




    @staticmethod
    def from_dict(data_dict):
        return Prescription(
            id = data_dict.get('_id', None),
            client_id = data_dict.get('client_id', None),
            given_date = data_dict.get('given_date', None),
            expiration_date = data_dict.get('expiration_date', None),
            hospital = data_dict.get('hospital', None),
            doctor = data_dict.get('doctor', None),
            drug_name = data_dict.get('drug_name', None),
            max_given = data_dict.get('max_given', None),
            given_nb = data_dict.get('given_nb', 0)
        )

    def to_dict(self):
        data = {
            'client_id': self.client_id,
            'given_date': datetime.combine(self.given_date, datetime.min.time()),
            'expiration_date': datetime.combine(self.expiration_date, datetime.min.time()),
            'drug_name': self.drug_name,
            'hospital': self.hospital,
            'doctor': self.doctor,
            'status': self.status,
            'max_given': self.max_given,
            'given_nb': self.given_nb
        }
        if self.id is not None:
            data['_id'] = self.id

        return data

    
    def create(self):
        try:
            inserted_prescrip = db.prescriptions.insert_one(self.to_dict())
            inserted_prescrip_id = str(inserted_prescrip.inserted_id)
            print(f"{inserted_prescrip_id} : inserted" )

            client_data = db.clients.find_one({'_id': ObjectId(self.client_id)})
            if client_data is None:
                print("no client found with this id")
                return False
            else:
                client_data['prescription_ids'].append(inserted_prescrip_id)
                db.clients.update_one({'_id': ObjectId(self.client_id)}, {'$set': {'prescription_ids': client_data['prescription_ids']}})
                print("client presctiptions updated")
                return True
        
        except Exception as e:
            print(e)
            return False  

    def update_status(self):
        new_status = self.status  # Obtenez le statut calculé par la propriété status
        try:
            # Mettez à jour le statut dans la base de données
            db.prescriptions.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {'status': new_status}}
            )
            print(f"Prescription {self.id} status updated to {new_status}")
        except Exception as e:
            print(f"Failed to update status for Prescription {self.id}: {e}")  


    @staticmethod
    def get_all_prescriptions():
        try:
            prescription_dicts = list(db.prescriptions.find())
            return [Prescription.from_dict(prescription_dict) for prescription_dict in prescription_dicts]
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_prescriptions_by_client_id(client_id):
        try:
            prescription_dicts = list(db.prescriptions.find({'client_id': client_id}))
            if prescription_dicts is None:
                return None
            else:
                return [Prescription.from_dict(prescription_dict) for prescription_dict in prescription_dicts]
        except Exception as e:
            print(e)
            return []

    

    @staticmethod
    def get_prescription_by_id(prescription_id):
        try:
            prescription_dict = db.prescriptions.find_one({'_id': ObjectId(prescription_id)})
            if prescription_dict is None:
                return None
            return Prescription.from_dict(prescription_dict)
        except Exception as e:
            print(e)
            return None
    

    @staticmethod
    def increment_given_nb(prescription_id):
        try:
            prescription_data = db.prescriptions.find_one({'_id': ObjectId(prescription_id)})
            if prescription_data is None:
                print(f"No prescription found with id: {prescription_id}")
                return False
            else:
                updated_given_nb = prescription_data.get('given_nb', 0) + 1
                if updated_given_nb > prescription_data.get('max_given', 0):
                    print(f"Prescription {prescription_id} has reached its maximum given number.")
                    return False
                db.prescriptions.update_one(
                    {'_id': ObjectId(prescription_id)},
                    {'$set': {'given_nb': updated_given_nb}}
                )
                return True
        except Exception as e:
            print(e)
            return False



