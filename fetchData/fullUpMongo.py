from IA_pretest.models.adresse import Adresse
from IA_pretest.models.client import Client
from IA_pretest.models.drug import Drug
from IA_pretest.models.prescription import Prescription
from IA_pretest.models.sell import Sell


from faker import Faker
from dateutil.relativedelta import relativedelta
from dateutil import parser

import random
import datetime
import time

fake = Faker()


drug_names = ["Atorvastatine", "Rosuvastatine", "Omeprazole",
                   "Levothyroxine", "Metformine", "Amlodipine", "Metoprolol", 
                    "Alprazolam", "Sertraline", "Zolpidem", "Hydrochlorothiazide",
                    "Lisinopril", "Esomeprazole", "Simvastatin", "Clopidogrel",
                    "Montelukast", "Pantoprazole", "Losartan", "Venlafaxine",
                    "Warfarin", "Pravastatin", "Fluticasone", "Quetiapine",
                    "Tramadol", "Bupropion", "Gabapentin", "Citalopram",
                    "Trazodone", "Atorvastatin", "Donepezil"]

def format_time(seconds):
    minutes = int(seconds) // 60
    seconds = int(seconds) % 60
    return f"{minutes} minutes {seconds} secondes"

def generate_door_number():
    # Choisissez un nombre aléatoire de chiffres entre 2 et 5
    num_digits = random.randint(2, 5)
    # Générez un numéro de porte aléatoire avec le nombre choisi de chiffres
    door_number = random.randint(10**(num_digits-1), 10**num_digits - 1)
    return door_number



def create_clients(n_client):
    for i in range (n_client):
        first_name=fake.first_name()
        last_name=fake.last_name()
        age=fake.random_int(min=18, max=100)
        sexe=fake.random_element(elements=('M', 'F'))
        email=fake.email()
        email_client = Client.get_client_by_email(email)
        while email_client is not None:
            email=fake.email()
        phone=fake.phone_number()
    
        fake_client = Client(
            first_name = first_name,
            last_name = last_name,
            age = age,
            sexe = sexe,
            email = email,
            phone = phone,
        )
        fake_client.create()

def create_adresses():
    existing_clients = Client.get_all_clients()
    print (f"{existing_clients} found")
    if not existing_clients:
        print("Aucun client trouvé. Assurez-vous d'avoir créé des clients avant de générer des adresses.")
        return False

    for client in existing_clients:
        print (f"{client.first_name} adress process...")
        # Décidez aléatoirement si ce client reçoit une, deux ou trois adresses
        additional_addresses = random.randint(1, 3)
        print(f"number of adress is {additional_addresses}")
        
        for _ in range(additional_addresses):
            door = generate_door_number()
            street = fake.street_name()
            city = fake.city()
            postal_code = fake.postcode()
            state = fake.state()
            country = fake.country()
            
            # Créez une instance de l'objet Adresse
            new_adresse = Adresse(
                door=door,
                street=street,
                city=city,
                postal_code=postal_code,
                state=state,
                country=country,
                client_ids=[client.id]  # Attribuez cette adresse au client actuel
            )
            print (f"{new_adresse}")
            # Enregistrez l'adresse dans la base de données
            new_adresse.create(client.id)
            
 

def create_drugs():
    
    for drug_name in drug_names:

        name = drug_name
        stock = 2000
        buy_price = round(random.uniform(6.00, 115.00), 2)
        profit_range = round(random.uniform(1.5, 2.4), 2)
        sell_price = round(buy_price * profit_range, 2)

        drug = Drug(
            name = name,
            stock = stock,
            buy_price = buy_price,
            sell_price = sell_price,            
        )
        drug.create()




def create_prescriptions():
    existing_clients = Client.get_all_clients()
    if not existing_clients:
        print("Aucun client trouvé. Assurez-vous d'avoir créé des clients avant de générer des adresses.")
        return False
    
    for client in existing_clients:
        
        nb_prescription = random.randint(1, 16)

        for i in range(nb_prescription):
            client_id = client.id
            today = datetime.datetime.today()
            year_ago = today - relativedelta(years=1)

            # Décider si la prescription sera active ou expirée
            is_active = random.random() < 0.8  # 80% de chance d'être active

            if is_active:
                # Pour les prescriptions actives
                #date between today and 2 months ago
                two_months_ago = datetime.datetime.today() - relativedelta(months=2)
                given_date = fake.date_between(start_date=two_months_ago, end_date=today)
            else:
                # Pour les prescriptions expirées
                given_date = fake.date_between(start_date=year_ago, end_date=today - relativedelta(months=6))
            
            expiration_date = fake.date_between(start_date=given_date, end_date=today + relativedelta(days=random.randint(30, 180)))
            drug_name = random.choice(drug_names)
            hospital = fake.company()
            doctor = fake.name()
            max_given = random.randint(1, 6)
            given_nb = 0

            new_prescripton  = Prescription(
                client_id = client_id,
                given_date = given_date,
                expiration_date = expiration_date,
                drug_name = drug_name,
                hospital = hospital,
                doctor = doctor,
                max_given = max_given,
                given_nb = given_nb
            )
            new_prescripton.create()




def create_sells():
    existing_clients = Client.get_all_clients()
    if not existing_clients:
        print("Aucun client trouvé. Assurez-vous d'avoir créé des clients avant de générer des ventes.")
        return False

    for client in existing_clients:
        print(f"{client.first_name} sell process...")
        num_sells = random.randint(1, 32)  # Nombre aléatoire de ventes
        print(f"number of sells is {num_sells}")

        for i in range(num_sells):
            client_prescriptions = Prescription.get_prescriptions_by_client_id(client.id)
            if not client_prescriptions:
                print("Aucune prescription trouvée pour ce client. Assurez-vous d'avoir créé des prescriptions avant de générer des ventes.")
                continue  # Utilisez continue plutôt que return False pour passer au client suivant

            active_prescriptions = [prescrip for prescrip in client_prescriptions if prescrip.status == 'active']
            if not active_prescriptions:
                print("Aucune prescription active trouvée pour ce client.")
                continue

            # Nombre aléatoire de prescriptions par vente, ne peut pas dépasser le nombre de prescriptions actives
            num_prescriptions_per_sell = random.randint(1, len(active_prescriptions))

            # Sélection aléatoire des prescriptions pour cette vente
            selected_prescriptions = random.sample(active_prescriptions, num_prescriptions_per_sell)

            # Obtenez les IDs des prescriptions sélectionnées
            selected_prescription_ids = [prescrip.id for prescrip in selected_prescriptions]

            # Date aléatoire pour la vente entre la date de la première prescription et la date d'expiration de la dernière prescription
            sell_date = fake.date_between(start_date=selected_prescriptions[0].given_date, end_date=datetime.datetime.today())
            sell_datetime = datetime.datetime.combine(sell_date, datetime.time.min)
            # Créer l'objet Sell
            sell = Sell(
                date=sell_datetime,
                client_id=client.id,
                prescription_ids=selected_prescription_ids
            )
            sell.create()

    return True  


                
                    
def create_all():
    start_time_all = time.time()
    
    create_adresses()

    time_adresses = time.time() - start_time_all

    create_prescriptions()

    time_prescriptions = time.time() - time_adresses

    create_sells()

    time_sells = time.time() - time_prescriptions
    total_time = time.time() - start_time_all

    total_time_str = format_time(total_time)
    time_adresses_str = format_time(time_adresses)
    time_prescriptions_str = format_time(time_prescriptions)
    time_sells_str = format_time(time_sells)

    print(f"Données générées avec succès en {total_time_str} !\n"
        f"Temps d'exécution de create_adresses : {time_adresses_str}\n"
        f"Temps d'exécution de create_prescriptions : {time_prescriptions_str}\n"
        f"Temps d'exécution de create_sells : {time_sells_str}")







#create_drugs()
#create_clients(4)
create_all()


#create_adresses()

#create_prescriptions()
#create_sells()


#print(Sell.get_all_sells())