from database.mongoDB import connection


import pandas as pd
import csv
import time

# Établissez une connexion à MongoDB
db = connection()

def fetch_data():
    pipeline = [
        {
            "$lookup": {
                "from": "prescriptions",
                "localField": "_id",
                "foreignField": "client_id",
                "as": "prescriptions"
            }
        },
        {
            "$lookup": {
                "from": "sells",
                "localField": "_id",
                "foreignField": "client_id",
                "as": "sells"
            }
        },
        {
            "$unwind": "$prescriptions"
        },
        {
            "$lookup": {
                "from": "drugs",
                "localField": "prescriptions.drug_name",
                "foreignField": "name",
                "as": "drug_info"
            }
        },
        {
            "$unwind": "$drug_info"
        },
        {
            "$unwind": "$sells"
        },
        {
            "$addFields": {
                "Profit": {
                    "$round": [
                        {
                            "$subtract": ["$drug_info.sell_price", "$drug_info.buy_price"]
                        },
                        2
                    ]
                }
            }
        },
        {
            "$project": {
                "Client ID": "$_id",
                "Age": "$age",
                "Sexe": "$sexe",
                "PrescriptionGivenDate": "$prescriptions.given_date",
                "PrescriptionExpirationDate": "$prescriptions.expiration_date",
                "DrugName": "$prescriptions.drug_name",
                "PrescriptionStatus": "$prescriptions.status",
                "PrescriptionMaxGiven": "$prescriptions.max_given",
                "PrescriptionGivenNb": "$prescriptions.given_nb",
                "SellDate": "$sells.date",
                "Profit": "$Profit",
                "Sell Prescription IDs": {
                    "$map": {
                        "input": "$sells.prescription_ids",
                        "as": "prescription_id",
                        "in": { "$toString": "$$prescription_id"}
                    }
                }
            }
        }
    ]
    cursor = db.clients.aggregate(pipeline)
    return list(cursor)



def export_to_csv(data, output_file):
    keys = data[0].keys()
    print(f"export_to_csv function keys")
    while_start_time = time.time()
    with open(output_file, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    while_time = time.time() - while_start_time
    print(f'Données exportées vers {output_file}')
    print(f"while_time : {while_time}")

start_time = time.time()

data = fetch_data()
fetch_time = time.time() - start_time
print(f"fetch_time : {fetch_time}")

export_to_csv(data, 'outputMongoDB.csv')

total_time = time.time() - start_time
print(f"total_time : {total_time}")
