import streamlit as st
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from datetime import datetime, timedelta
import random
import mysql.connector 


def get_cursor():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pharmaai"
    )
    cursor = connection.cursor(dictionary=True)  
    return cursor, connection

def get_all_drugs():
    cursor, connection = get_cursor()
    query = "SELECT * FROM drugs"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_all_clients():
    cursor, connection = get_cursor()
    query = "SELECT * FROM clients"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_all_prescriptions():
    cursor, connection = get_cursor()
    query = "SELECT * FROM prescriptions"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_all_sells():
    cursor, connection = get_cursor()
    query = "SELECT * FROM sells"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results






def add_data():
    existing_csv = "outputSQL.csv"

    add_options = ["Choisi une option", "Ajouter une transaction", "Ajouter plusieurs transactions"]
    selected_option = st.selectbox("Choisir une option", add_options)


    if selected_option == "Ajouter une transaction":
        # Obtenir les informations nécessaires depuis la base de données
        drugs = get_all_drugs()
        clients = get_all_clients()
        prescriptions = get_all_prescriptions()
        sells = get_all_sells()

        # fing hightes sell_id in get_all_sells()
        sell_id = max([sell['sell_id'] for sell in sells]) + 1
        # Limiter la liste des clients à un maximum de 15 éléments

        email_input = st.text_input("Rechercher un client par email")

        # Filtrer les clients basé sur l'input
        filtered_clients = [client for client in clients if email_input.lower() in client['email'].lower()]

        # Option modifiée pour sélectionner un client
        if filtered_clients:
            client_options = {client['client_id']: client['first_name'] for client in filtered_clients}
            client_id = st.selectbox("Choisir un client", list(client_options.keys()), format_func=lambda x: client_options[x])
            selected_client = next((client for client in clients if client['client_id'] == client_id), None)
        else:
            st.write("Aucun client trouvé avec cet email.")
            selected_client = None

        if selected_client:
            # Votre logique ici, par exemple :
            client_sex = selected_client['sexe']
            client_age = selected_client['age']
        else:
            st.error("Sélectionnez un client valide.")


        # Extraire le sexe du client sélectionné
        client_sex = selected_client['sexe']
        client_age = selected_client['age']

        # Supposons que sell_date est déjà définie via st.date_input
        sell_date = st.date_input("Date de vente", datetime.now())
        # Générer une date aléatoire pour prescription_given_date entre sell_date et 5 jours ou moins
        prescription_given_date = sell_date - timedelta(days=random.randint(0, 5))
        # Générer une date aléatoire pour PrescriptionExpirationDate entre prescription_given_date + 30 jours et prescription_given_date + 90 jours
        PrescriptionExpirationDate = prescription_given_date + timedelta(days=random.randint(30, 90))
        # Générer un entier aléatoire pour PrescriptionGivenNb entre 1 et 5
        PrescriptionGivenNb = random.randint(1, 5)
        # Générer un entier aléatoire pour PrescriptionMaxGiven entre PrescriptionGivenNb et PrescriptionGivenNb + 5
        PrescriptionMaxGiven = random.randint(PrescriptionGivenNb + 1, PrescriptionGivenNb + 5)
        # Affichage des valeurs pour vérification
        st.write("Date de vente:", sell_date)
        st.write("Date de délivrance de la prescription:", prescription_given_date)
        st.write("Date d'expiration de la prescription:", PrescriptionExpirationDate)
        st.write("Nombre de prescriptions données:", PrescriptionGivenNb)
        st.write("Nombre maximal de prescriptions données:", PrescriptionMaxGiven)
   
        PrescriptionStatus = "active"
        
        # Sélection du médicament par l'utilisateur
        drugName = st.selectbox("Choisir un médicament", [drug['name'] for drug in drugs])

        # Trouver le médicament sélectionné dans la liste pour obtenir ses prix
        selected_drug = next((drug for drug in drugs if drug['name'] == drugName), None)

        if selected_drug:
            # Extraction des prix de vente et d'achat
            sellPrice = selected_drug['sell_price']
            buyPrice = selected_drug['buy_price']

            # Affichage des prix pour vérification
            st.write("Prix de vente:", sellPrice)
            st.write("Prix d'achat:", buyPrice)
        else:
            st.write("Médicament non trouvé.")
            
        # Calcul des attributs
        sellDayOfWeek = sell_date.strftime('%A')  # Nom du jour de la semaine
        sellDayOfMonth = sell_date.day
        sellMonth = sell_date.month
        sellYear = sell_date.year
        SellDateIsWeekend = sell_date.weekday() >= 5  # True si c'est samedi (5) ou dimanche (6)

        # Détermination si la date est un jour férié
        cal = USFederalHolidayCalendar()
        holidays = cal.holidays(start=sell_date, end=sell_date)
        SellDateIsHoliday = not holidays.empty  # True si la date est un jour férié

        # Détermination de la saison
        if sellMonth in [12, 1, 2]:
            SellDateSeason = "Winter"
        elif sellMonth in [3, 4, 5]:
            SellDateSeason = "Spring"
        elif sellMonth in [6, 7, 8]:
            SellDateSeason = "Summer"
        else:
            SellDateSeason = "Fall"

        # Calcul des attributs
        PrescriptionGivenDayOfWeek = prescription_given_date.strftime('%A')  # Nom du jour de la semaine
        PrescriptionGivenDay = prescription_given_date.day
        PrescriptionGivenMonth = prescription_given_date.month
        PrescriptionGivenYear = prescription_given_date.year
        PrescriptiongivenDateIsWeekend = prescription_given_date.weekday() >= 5  # True si c'est samedi (5) ou dimanche (6)

        # Détermination si la date est un jour férié
        cal = USFederalHolidayCalendar()
        holidays = cal.holidays(start=prescription_given_date, end=prescription_given_date)
        PrescriptiongivenDateIsHoliday = not holidays.empty  # True si la date est un jour férié

        # Détermination de la saison
        if PrescriptionGivenMonth in [12, 1, 2]:
            PrescriptionGivenSeason = "Winter"
        elif PrescriptionGivenMonth in [3, 4, 5]:
            PrescriptionGivenSeason = "Spring"
        elif PrescriptionGivenMonth in [6, 7, 8]:
            PrescriptionGivenSeason = "Summer"
        else:
            PrescriptionGivenSeason = "Fall"

        PrescriptionExpirationDayOfWeek = PrescriptionExpirationDate.strftime('%A')
        PrescriptionExpirationDay = PrescriptionExpirationDate.day
        PrescriptionExpirationMonth = PrescriptionExpirationDate.month
        PrescriptionExpirationYear = PrescriptionExpirationDate.year
        PrescriptionExpirationDateIsWeekend = PrescriptionExpirationDate.weekday() >= 5
        holidays = cal.holidays(start=PrescriptionExpirationDate, end=PrescriptionExpirationDate)
        PrescriptionExpirationDateIsHoliday = not holidays.empty 
        
        if PrescriptionExpirationMonth in [12, 1, 2]:
            PrescriptionExpirationSeason = "Winter"
        elif PrescriptionExpirationMonth in [3, 4, 5]:
            PrescriptionExpirationSeason = "Spring"
        elif PrescriptionExpirationMonth in [6, 7, 8]:
            PrescriptionExpirationSeason = "Summer"
        else:
            PrescriptionExpirationSeason = "Fall"
        
        Profit = sellPrice - buyPrice
        
        

        if (st.button("Ajouter", key="btn_add_one")):
            df_existing = pd.read_csv(existing_csv)

            # Ajouter une nouvelle ligne
            new_row = {
                'id_vente' : sell_id,
                'id_client': client_id,
                "sexe": client_sex,
                "age": client_age,
                'SellDate': sell_date,
                'PrescriptionGivenDate': prescription_given_date,
                'PrescriptionExpirationDate': PrescriptionExpirationDate,
                'PrescriptionGivenNb': PrescriptionGivenNb,
                'PrescriptionMaxGiven': PrescriptionMaxGiven,
                'PrescriptionStatus': PrescriptionStatus,
                'DrugName':drugName,
                'SellPrice': sellPrice,
                'BuyPrice': buyPrice,
                'SellDayOfWeek': sellDayOfWeek,
                'SellDayOfMonth': sellDayOfMonth,
                'SellMonth': sellMonth,
                'SellYear': sellYear,
                'SellDateIsWeekend': SellDateIsWeekend,
                'SellDateIsHoliday': SellDateIsHoliday,
                'SellDateSeason': SellDateSeason,
                'PrescriptionGivenDayOfWeek': PrescriptionGivenDayOfWeek,
                'PrescriptionGivenDay': PrescriptionGivenDay,
                'PrescriptionGivenMonth': PrescriptionGivenMonth,
                'PrescriptionGivenYear': PrescriptionGivenYear,
                'PrescriptiongivenDateIsWeekend': PrescriptiongivenDateIsWeekend,
                'PrescriptiongivenDateIsHoliday': PrescriptiongivenDateIsHoliday,
                'PrescriptionGivenSeason': PrescriptionGivenSeason,
                'PrescriptionExpirationDayOfWeek': PrescriptionExpirationDayOfWeek,
                'PrescriptionExpirationDay': PrescriptionExpirationDay,
                'PrescriptionExpirationMonth': PrescriptionExpirationMonth,
                'PrescriptionExpirationYear': PrescriptionExpirationYear,
                'PrescriptionExpirationDateIsWeekend': PrescriptionExpirationDateIsWeekend,
                'PrescriptionExpirationDateIsHoliday': PrescriptionExpirationDateIsHoliday,
                'PrescriptionExpirationSeason': PrescriptionExpirationSeason,
                'Profit': Profit
                }

            df_existing = df_existing.append(new_row, ignore_index=True)

            # Sauvegarder le DataFrame modifié dans le fichier CSV
            df_existing.to_csv(existing_csv, index=False)

            st.success("Transaction ajoutée avec succès")

    elif selected_option == "Ajouter plusieurs transactions":
        csv_file = st.file_uploader("Choisir un fichier CSV", type="csv")

        if st.button("Ajouter", key="btn_add_multiple"):
            if csv_file:
                # Spécification des types pour les colonnes connues
                dtype_spec = {
                    'id_vente': int,
                    'id_client': int,
                    'age': int,
                    'SellPrice': float,
                    'BuyPrice': float,
                    # Ajoutez ou modifiez les colonnes selon vos besoins
                }
                df_new_data = pd.read_csv(csv_file, dtype=dtype_spec)
                df_existing = pd.read_csv(existing_csv, dtype=dtype_spec)

                # Concaténer les nouveaux et anciens DataFrames
                df_existing = pd.concat([df_existing, df_new_data], ignore_index=True)

                # Sauvegarder le DataFrame modifié
                df_existing.to_csv(existing_csv, index=False)
                st.success("Transactions ajoutées avec succès")
