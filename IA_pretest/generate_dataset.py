import pandas as pd
from datetime import datetime, timedelta
import random
from pandas.tseries.holiday import USFederalHolidayCalendar


# Fonction pour générer des données fictives adéquates avec les colonnes spécifiées
def generate_fake_data(num_rows=10):
    # Liste des colonnes du dataset
    columns = [
        "id_vente", "id_client", "sexe", "age", "SellDate", "PrescriptionGivenDate",
        "PrescriptionExpirationDate", "PrescriptionGivenNb", "PrescriptionMaxGiven",
        "PrescriptionStatus", "DrugName", "SellPrice", "BuyPrice", "SellDayOfWeek",
        "SellDayOfMonth", "SellMonth", "SellYear", "SellDateIsWeekend", "SellDateIsHoliday",
        "SellDateSeason", "PrescriptionGivenDayOfWeek", "PrescriptionGivenDay", "PrescriptionGivenMonth",
        "PrescriptionGivenYear", "PrescriptiongivenDateIsWeekend", "PrescriptiongivenDateIsHoliday",
        "PrescriptionGivenSeason", "PrescriptionExpirationDayOfWeek", "PrescriptionExpirationDay",
        "PrescriptionExpirationMonth", "PrescriptionExpirationYear", "PrescriptionExpirationDateIsWeekend",
        "PrescriptionExpirationDateIsHoliday", "PrescriptionExpirationSeason", "Profit"
    ]
    
    
    
    
    # Création des dictionnaires pour les prix et profits des médicaments basés sur les nouvelles informations fournies

    buy_price_drugs = {
        "Atorvastatine": 15.13,
        "Rosuvastatine": 33.17,
        "Omeprazole": 52.67,
        "Levothyroxine": 53.82,
        "Metformine": 114.27,
        "Amlodipine": 16.30,
        "Metoprolol": 68.95,
        "Alprazolam": 110.20,
        "Sertraline": 21.37,
        "Zolpidem": 60.69,
        "Hydrochlorothiazide": 101.50,
        "Lisinopril": 45.76,
        "Esomeprazole": 81.94,
        "Simvastatin": 17.33,
        "Clopidogrel": 43.67,
        "Montelukast": 93.55,
        "Pantoprazole": 68.33,
        "Losartan": 101.57,
        "Venlafaxine": 52.24,
        "Warfarin": 52.04,
        "Pravastatin": 11.64,
        "Fluticasone": 84.24,
        "Quetiapine": 102.07,
        "Tramadol": 20.56,
        "Bupropion": 94.35
    }
    
    drugs = (['Atorvastatine', 'Rosuvastatine', 'Omeprazole', 'Levothyroxine', 'Metformine', 'Amlodipine',
                     'Metoprolol', 'Alprazolam', 'Sertraline', 'Zolpidem', 'Hydrochlorothiazide', 'Lisinopril',
                        'Esomeprazole', 'Simvastatin', 'Clopidogrel', 'Montelukast', 'Pantoprazole', 'Losartan',
                        'Venlafaxine', 'Warfarin', 'Pravastatin', 'Fluticasone', 'Quetiapine', 'Tramadol', 'Bupropion'])
    


    sell_price_drugs = {
        "Atorvastatine": 29.96,
        "Rosuvastatine": 75.63,
        "Omeprazole": 122.19,
        "Levothyroxine": 109.79,
        "Metformine": 198.83,
        "Amlodipine": 31.30,
        "Metoprolol": 146.86,
        "Alprazolam": 204.97,
        "Sertraline": 36.54,
        "Zolpidem": 123.81,
        "Hydrochlorothiazide": 227.36,
        "Lisinopril": 86.94,
        "Esomeprazole": 149.95,
        "Simvastatin": 30.67,
        "Clopidogrel": 87.78,
        "Montelukast": 166.52,
        "Pantoprazole": 153.74,
        "Losartan": 204.16,
        "Venlafaxine": 94.03,
        "Warfarin": 106.16,
        "Pravastatin": 22.93, 
        "Fluticasone": 174.38,
        "Quetiapine": 221.49,
        "Tramadol": 46.47,
        "Bupropion": 215.12
    }

    def determine_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'

    # Liste pour stocker les données générées
    data = []


    def is_holiday(date, holidays):
        return date in holidays
    
    cal = USFederalHolidayCalendar()
    holidays = cal.holidays(start='2020-01-01', end='2030-12-31')
    
    # Générer num_rows de données
    for _ in range(num_rows):
        # Choix aléatoire d'un médicament
        drug_name = random.choice(drugs)
    
        # Récupération du prix de vente du médicament choisi
        sell_price = sell_price_drugs[drug_name]
        buy_price = buy_price_drugs[drug_name]
        # Calcul du prix d'achat basé sur le profit souhaité pour le médicament choisi
        profit = sell_price - buy_price
    
        # Autres attributs générés comme avant
        sell_date = datetime.now() - timedelta(days=random.randint(1, 365))
        prescription_given_date = sell_date - timedelta(days=random.randint(1, 30))
        prescription_expiration_date = sell_date + timedelta(days=random.randint(30, 90))

        row = [
            random.randint(2, 6574),  # id_vente
            random.randint(1, 960),  # id_client
            random.choice(["M", "F"]),  # sexe
            random.randint(18, 100),  # age
            sell_date.strftime('%Y-%m-%d'),  # SellDate
            prescription_given_date.strftime('%Y-%m-%d'),  # PrescriptionGivenDate
            prescription_expiration_date.strftime('%Y-%m-%d'),  # PrescriptionExpirationDate
            random.randint(1, 5),  # PrescriptionGivenNb
            random.randint(5, 10),  # PrescriptionMaxGiven
            random.choice(['active', 'expired']),  # PrescriptionStatus
            drug_name,  # DrugName
            sell_price,  # SellPrice
            buy_price,  # BuyPrice
            sell_date.strftime('%A'),  # SellDayOfWeek
            sell_date.day,  # SellDayOfMonth
            sell_date.month,  # SellMonth
            sell_date.year,  # SellYear
            sell_date.weekday() >= 5,  # SellDateIsWeekend
            is_holiday(sell_date, holidays),  # SellDateIsHoliday (simplification)
            determine_season(sell_date.month),  # SellDateSeason (simplification)
            prescription_given_date.strftime('%A'),  # PrescriptionGivenDayOfWeek
            prescription_given_date.day,  # PrescriptionGivenDay
            prescription_given_date.month,  # PrescriptionGivenMonth
            prescription_given_date.year,  # PrescriptionGivenYear
            prescription_given_date.weekday() >= 5,  # PrescriptiongivenDateIsWeekend
            is_holiday(prescription_given_date, holidays),  # PrescriptiongivenDateIsHoliday (simplification)
            determine_season(prescription_given_date.month),  # PrescriptionGivenSeason (simplification)
            prescription_expiration_date.strftime('%A'),  # PrescriptionExpirationDayOfWeek
            prescription_expiration_date.day,  # PrescriptionExpirationDay
            prescription_expiration_date.month,  # PrescriptionExpirationMonth
            prescription_expiration_date.year,  # PrescriptionExpirationYear
            prescription_expiration_date.weekday() >= 5,  # PrescriptionExpirationDateIsWeekend
            is_holiday(prescription_expiration_date, holidays),  # PrescriptionExpirationDateIsHoliday (simplification)
            determine_season(prescription_expiration_date.month),   # PrescriptionExpirationSeason (simplification)
            round(profit, 2)  # Profit
        ]

        data.append(row)
    
    existing_df = pd.read_csv('outputSQL.csv')
    existing_df['id_vente'] = existing_df['id_vente'].astype(int)

    # Créer un DataFrame à partir des données générées
    df = pd.DataFrame(data, columns=columns)
    df.to_csv( 'generate_output.csv', index=False)

generate_fake_data(10)
