from database.sql import get_cursor
from models.drug import Drug
from models.client import Client
from models.adresse import Adresse
from models.prescription import Prescription
from models.sell import Sell

import time
import traceback

cursor, connection = get_cursor()
client_id_mapping = {}
prescription_id_mapping = {}


def migrate_all():
    drug_counter = 0  # Compteur pour le débogage
    client_counter = 0
    address_counter = 0
    prescription_counter = 0
    sell_counter = 0
    
    try:
        # Migrate drugs
        all_drugs = Drug.get_all_drugs()
        insert_drug_query = """
        INSERT INTO drugs (mongo_id, name, stock, buy_price, sell_price) 
        VALUES (%s, %s, %s, %s, %s)
        """
        for drug in all_drugs:

            drug_data = (
                str(drug.id),
                drug.name,
                drug.stock,
                drug.buy_price,
                drug.sell_price
            )
            cursor.execute(insert_drug_query, drug_data)
            drug_counter += 1
        connection.commit()
        print('All drugs inserted')

        # Migrate clients and addresses
        all_clients = Client.get_all_clients()
        insert_client_query = "INSERT INTO clients (mongo_id, first_name, last_name, age, sexe, email, phone) VALUES (%s, %s, %s, %s, %s, %s)"
                # Migrate clients and addresses
        all_clients = Client.get_all_clients()
        insert_client_query = """
        INSERT INTO clients (mongo_id, first_name, last_name, age, sexe, email, phone) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        insert_address_query = """
        INSERT INTO adresses (mongo_id, door, street, 
        city, postal_code, state, country, client_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        insert_client_addresses_query = """
        INSERT INTO client_addresses (client_id, address_id)
        VALUES (%s, %s)
        """

        for client in all_clients:
            client_data = (
                str(client.id),
                client.first_name,
                client.last_name,
                client.age,
                client.sexe,
                client.email,
                client.phone
            )
            cursor.execute(insert_client_query, client_data)
            client_id = cursor.lastrowid  # Get the auto-generated ID for the client
            client_id_mapping[str(client.id)] = client_id
            client_counter += 1

            client_addresses = Adresse.get_adress_by_client_id(client.id)
            for address in client_addresses:
                address_data = (
                    str(address.id),
                    address.door,
                    address.street,
                    address.city,
                    address.postal_code,
                    address.state,
                    address.country,
                    client_id
                )
                cursor.execute(insert_address_query, address_data)
                address_id = cursor.lastrowid  # Get the auto-generated ID for the address

                # Now insert the association into client_addresses
                cursor.execute(insert_client_addresses_query, (client_id, address_id))
                address_counter += 1

        connection.commit()
        print(f'Inserted {client_counter} clients and {address_counter} addresses with their associations.')


        # Migration des prescriptions
        all_prescriptions = Prescription.get_all_prescriptions()
        insert_prescription_query = """
        INSERT INTO prescriptions (
            mongo_id, client_id, drug_id, given_date, expiration_date, 
            hospital, doctor, status, max_given, given_nb)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for prescription in all_prescriptions:
            print(prescription.id)
            client_id_sql = client_id_mapping.get(str(prescription.client_id))
            drug = Drug.get_drug_by_name(prescription.drug_name)

            select_drug_query = """
            SELECT drug_id FROM drugs WHERE name = %s
            """
            cursor.execute(select_drug_query, (prescription.drug_name,))
            result = cursor.fetchone()  # Fetch the result of the query
            drug_id_sql = result[0] if result else None 

            if client_id_sql and drug_id_sql:
                # Formatage des dates pour l'insertion SQL
                formatted_given_date = prescription.given_date.strftime('%Y-%m-%d %H:%M:%S')
                formatted_expiration_date = prescription.expiration_date.strftime('%Y-%m-%d %H:%M:%S')

                prescription_data = (
                    str(prescription.id),
                    client_id_sql, 
                    drug_id_sql, 
                    formatted_given_date, 
                    formatted_expiration_date,
                    prescription.hospital, 
                    prescription.doctor, 
                    prescription.status,
                    prescription.max_given, 
                    prescription.given_nb
                )
                cursor.execute(insert_prescription_query, prescription_data)
                
                prescription_counter += 1
                prescription_id_sql = cursor.lastrowid
                prescription_id_mapping[str(prescription.id)] = prescription_id_sql
                print(f'Inserted prescription with ID {prescription_id_sql} for client {client_id_sql}')
        connection.commit()
        print(f'Inserted {prescription_counter} prescriptions.')

        # Migration des ventes
        all_sells = Sell.get_all_sells()
        insert_sell_query = "INSERT INTO sells (mongo_id, client_id, date, total) VALUES (%s, %s, %s, %s)"
        insert_sell_prescriptions_query = "INSERT INTO sell_prescriptions (sell_id, prescription_id) VALUES (%s, %s)"
        for sell in all_sells:
            print(f"Processing sell {sell.id}")
            select_client_query = """
            SELECT client_id FROM clients WHERE mongo_id = %s
            """
            cursor.execute(select_client_query, (str(sell.client_id),))
            result = cursor.fetchone()

            # This is a good place to check if the client ID was found
            if result:
                print(result)
                client_id_sql = result[0]
                print(f"Found client_id_sql: {client_id_sql}")
            else:
                # If no result, there is a problem with the client ID mapping
                print(f"No SQL client_id found for MongoDB client_id: {sell.client_id}")
                continue
            print(f"client id sql : {client_id_sql}") # Extract the client_id if a result was found

            if client_id_sql:  # Ensure you have a client_id before attempting to insert
                formatted_date = sell.date.strftime('%Y-%m-%d %H:%M:%S')
                sell_data = (
                    str(sell.id),
                    formatted_date, 
                    client_id_sql,
                    sell.total
                )
                print(f"sell data : {sell_data}")

                # Now insert the sell record into the sells table
                cursor.execute(insert_sell_query, sell_data)
                print(f"sell {sell.id} inserted!!!")
                sell_id_sql = cursor.lastrowid  # Get the auto-generated ID for the sell

                # Insertion des prescriptions associées à la vente
                for prescription_id in sell.prescription_ids:
                    # Assuming you have a mapping of MongoDB prescription ids to SQL ids
                    prescription_id_sql = str(prescription_id)
                    if prescription_id_sql:
                        print(f"Prescription id sql : {prescription_id_sql}")
                        cursor.execute(insert_sell_prescriptions_query, (sell_id_sql, prescription_id_sql))

                print(f'Inserted sell with ID {sell_id_sql} for client {client_id_sql}')
                sell_counter += 1

    except Exception as e:
        connection.rollback()
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()
        print("Database connection closed.")
    
    print("Migration completed successfully!")
    print(f"""
          Drugs : {drug_counter},\n
          Clients : {client_counter},\n
          Address : {address_counter},\n
          Prescriptions : {prescription_counter},\n
          Sells : {sell_counter}
        """
    )


def migrate_sells():
     # Migration des ventes
    try:
        sell_counter = 0
        all_sells = Sell.get_all_sells()

        insert_sell_query = "INSERT INTO sells (mongo_id, date, client_id, total) VALUES (%s, %s, %s, %s)"
        insert_sell_prescriptions_query = "INSERT INTO sell_prescriptions (sell_id, prescription_id) VALUES (%s, %s)"
        for sell in all_sells:
            print(f"Processing sell {sell.id}")
            #time.sleep(1)
            select_client_query = """
            SELECT client_id FROM clients WHERE mongo_id = %s
            """
            cursor.execute(select_client_query, (str(sell.client_id),))
            result = cursor.fetchone()

            # This is a good place to check if the client ID was found
            if result:
                client_id_sql = result[0]
                print(f"Found client_id_sql: {client_id_sql}")
                #time.sleep(1)
            else:
                # If no result, there is a problem with the client ID mapping
                print(f"No SQL client_id found for MongoDB client_id: {sell.client_id}")
                continue
            print(client_id_sql) # Extract the client_id if a result was found

            if client_id_sql:  # Ensure you have a client_id before attempting to insert
                formatted_date = sell.date.strftime('%Y-%m-%d %H:%M:%S')
                sell_data = (
                    str(sell.id),
                    formatted_date, 
                    client_id_sql,
                    sell.total                
                )
                print(f"sell data : {sell_data}")
                #time.sleep(1)
                # Now insert the sell record into the sells table
                cursor.execute(insert_sell_query, sell_data)
                print(f"sell {sell.id} inserted!!!")
                #time.sleep(1)
                sell_id_sql = cursor.lastrowid  # Get the auto-generated ID for the sell

                # Insertion des prescriptions associées à la vente
                for prescription_id in sell.prescription_ids:
                    prescription_id_sql = prescription_id_mapping.get(str(prescription_id))
                    print(prescription_id_sql)
                    if prescription_id_sql:

                        print(f"Prescription id sql : {prescription_id_sql}")
                       #time.sleep(1)
                        cursor.execute(insert_sell_prescriptions_query, (sell_id_sql, prescription_id_sql))
                        

                print(f'Inserted sell with ID {sell_id_sql} for client {client_id_sql}')
                #time.sleep(1)
                sell_counter += 1
                print(f'{sell_counter} sells inserted')
                #time.sleep(1)
                connection.commit()
    except Exception as e:
        traceback.print_exc()  # This will print the full traceback
        connection.rollback()
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()
        print("Database connection closed.")

def fill_up_sell_prescriptions():
    try:
        sell_prescription_counter = 0
        all_sells = Sell.get_all_sells()
        sell_id_mapping = {}  # Initialisation en tant que dictionnaire

        insert_sell_prescriptions_query = "INSERT INTO sell_prescriptions (sell_id, prescription_id) VALUES (%s, %s)"

        for sell in all_sells:
            print(f"Processing sell {sell.id}")
            sell_id_sql = sell_id_mapping.get(str(sell.id))
            if not sell_id_sql:
                cursor.execute("SELECT sell_id FROM sells WHERE mongo_id = %s", (str(sell.id),))
                result = cursor.fetchone()
                if result:
                    sell_id_sql = result[0]
                    sell_id_mapping[str(sell.id)] = sell_id_sql  # Stocker l'ID dans le mapping
                else:
                    print(f"sell_id not found for sell {sell.id}")
                    continue

            for prescription_id in sell.prescription_ids:
                query = "SELECT prescription_id FROM prescriptions WHERE mongo_id = %s"
                cursor.execute(query, (str(prescription_id),))
                prescription_id_sql = cursor.fetchone()[0]  
                if prescription_id_sql:
                    cursor.execute(insert_sell_prescriptions_query, (sell_id_sql, prescription_id_sql))
                    sell_prescription_counter += 1
                else:
                    print(f"Prescription_id not found for prescription {prescription_id}")

        connection.commit()
        print(f'Inserted {sell_prescription_counter} sell_prescription entries.')
    except Exception as e:
        traceback.print_exc()
        connection.rollback()
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Database connection closed.")




#migrate_all()
#migrate_sells()
fill_up_sell_prescriptions()