import pandas as pd
import random
from datetime import datetime, timedelta
from pandas.tseries.holiday import USFederalHolidayCalendar

def generate_dataset(n):

    medicaments = ["Paracétamol", "Ibuprofen", "Amoxicilline", "Aspirine", "Cortisone",
                   "Warfarine", "Metformine", "Amlodipine", "Simvastatine", "Omeprazole",
                   "Losartan", "Atorvastatine", "Azithromycine", "Hydrochlorothiazide",
                   "Furosemide", "Gabapentine", "Lisinopril", "Fluoxetine", "Prednisone",
                   "Sertraline", "Montelukast", "Esomeprazole", "Albuterol", "Venlafaxine",
                   "Duloxetine"]
                   
    prix_medicaments = {
        "Paracétamol": 5.0, "Ibuprofen": 6.0, "Amoxicilline": 8.0, "Aspirine": 3.5, "Cortisone": 7.5,
        "Warfarine": 10.0, "Metformine": 12.0, "Amlodipine": 14.0, "Simvastatine": 16.0, "Omeprazole": 5.5,
        "Losartan": 6.5, "Atorvastatine": 11.0, "Azithromycine": 13.0, "Hydrochlorothiazide": 15.0,
        "Furosemide": 17.0, "Gabapentine": 9.0, "Lisinopril": 5.0, "Fluoxetine": 7.0, "Prednisone": 3.5,
        "Sertraline": 6.5, "Montelukast": 8.5, "Esomeprazole": 4.5, "Albuterol": 9.5, "Venlafaxine": 10.5,
        "Duloxetine": 11.5
    }

    profit_medicaments = {
        "Paracétamol": 2.0, "Ibuprofen": 4.0, "Amoxicilline": 6.0, "Aspirine": 1.5, "Cortisone": 3.5,
        "Warfarine": 6.5, "Metformine": 8.25, "Amlodipine": 9.75, "Simvastatine": 12.0, "Omeprazole": 3.5,
        "Losartan": 2.5, "Atorvastatine": 6.5, "Azithromycine": 7.25, "Hydrochlorothiazide": 10.0,
        "Furosemide": 13.25, "Gabapentine": 4.0, "Lisinopril": 3.0, "Fluoxetine": 3.5, "Prednisone": 1.5,
        "Sertraline": 3.5, "Montelukast": 6.5, "Esomeprazole": 2.5, "Albuterol": 7.5, "Venlafaxine": 8.5,
        "Duloxetine": 5.5
    }

    
    cal = USFederalHolidayCalendar()
    holidays = cal.holidays(start='2020-01-01', end='2023-12-31').to_pydatetime()
    
    data = []
    for i in range(1, n+1):
        medicament = random.choice(medicaments)
        prix_unitaire = prix_medicaments[medicament]
        quantite = random.randint(1, 10)
        profit_unitaire = profit_medicaments[medicament]
        profit_ratio = profit_unitaire / prix_unitaire
        profit_total = profit_medicaments[medicament] * quantite
        profit_total_ratio = profit_total / (prix_unitaire * quantite)

        total = round(quantite * prix_unitaire, 2)
        #vendeur = random.choice(vendeurs)
        
        date = datetime.today() - timedelta(days=random.randint(0, 365))
        date_str = date.strftime('%Y-%m-%d')
        
        day_of_week = date.weekday()  # 0: Lundi, 1: Mardi, etc.
        day_of_month = date.day
        month = date.month
        year = date.year
        
        # Saison
        if month in [12, 1, 2]:
            saison = "Hiver"
        elif month in [3, 4, 5]:
            saison = "Printemps"
        elif month in [6, 7, 8]:
            saison = "Été"
        else:
            saison = "Automne"
        
        # Jour férié et weekend
        is_holiday = date in holidays
        is_weekend = day_of_week in [5, 6]  # 5: Samedi, 6: Dimanche
        
        # Ratio Prix/Quantité
        prix_quantite_ratio = round(prix_unitaire / quantite, 2)
        
        data.append({
            "Date" : date_str,
            "Medicament": medicament, 
            "Quantite": quantite, 
            "PrixUnitaire": prix_unitaire, 
            "ProfitUnitaire": profit_unitaire,
            "ProfitRatio" : profit_ratio,
            "Total": total, 
            "ProfitTotal": profit_total,
            "ProfitTotalRatio": profit_total_ratio,
            "DayOfWeek": day_of_week,
            "DayOfMonth": day_of_month, 
            "Month": month, 
            "Year": year,
            "Saison": saison,
            "IsHoliday": is_holiday, 
            "IsWeekend": is_weekend, 
            "PrixQuantiteRatio": prix_quantite_ratio
        })
        print (i, " data appended")
    df = pd.DataFrame(data)
   
    # Triez les données par date
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    
    # Statistiques roulantes (par exemple, moyenne sur 7 derniers jours)
    df['MoyenneRoulante_7d_Quantite'] = df['Quantite'].rolling(window=7).mean()
    
    df.to_csv( 'donnees_pharmacie_profit.csv', index=False)
    print("Dataframe created")


# Générer le dataset
generate_dataset(5000)
