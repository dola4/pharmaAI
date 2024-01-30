from datetime import datetime
from pandas.tseries.holiday import USFederalHolidayCalendar

from sql import get_cursor

import pandas as pd
import csv



cursor, connection = get_cursor()


# Établissement de la connexion à la base de données (remplacer par vos propres détails de connexion)
# Fonction pour déterminer la saison
def determine_season(month):
    if month in [1, 2, 12]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:  # 9, 10, 11
        return 'Fall'

# Exécuter la requête SQL
query = """
    SELECT
        s.sell_id AS id_vente,
        c.client_id AS id_client,
        c.sexe,
        c.age,
        s.date AS SellDate,
        p.given_date AS PrescriptionGivenDate,
        p.expiration_date AS PrescriptionExpirationDate,
        p.given_nb AS PrescriptionGivenNb,
        p.max_given AS PrescriptionMaxGiven,
        p.status AS PrescriptionStatus,
        d.name AS DrugName,
        d.sell_price AS SellPrice,
        d.buy_price AS BuyPrice
    FROM sells s
    JOIN sell_prescriptions sp ON s.sell_id = sp.sell_id
    JOIN prescriptions p ON sp.prescription_id = p.prescription_id
    JOIN clients c ON s.client_id = c.client_id
    JOIN drugs d ON p.drug_id = d.drug_id
"""
df = pd.read_sql(query, connection)

# Ajout des caractéristiques

cal = USFederalHolidayCalendar()
holidays = cal.holidays(start=df['SellDate'].min(), end=df['SellDate'].max())

df['SellDate'] = pd.to_datetime(df['SellDate'])
df['SellDayOfWeek'] = df['SellDate'].dt.day_name()
df['SellDayOfMonth'] = df['SellDate'].dt.day
df['SellMonth'] = df['SellDate'].dt.month
df['SellYear'] = df['SellDate'].dt.year
df['SellDateIsWeekend'] = df['SellDayOfWeek'].isin(['Saturday', 'Sunday'])
df['SellDateIsHoliday'] = df['SellDate'].isin(holidays)
df['SellDateSeason'] = df['SellMonth'].apply(determine_season)

df['PrescriptionGivenDate'] = pd.to_datetime(df['PrescriptionGivenDate'])
df['PrescriptionGivenDayOfWeek'] = pd.to_datetime(df['PrescriptionGivenDate']).dt.day_name()
df['PrescriptionGivenDay'] = df['PrescriptionGivenDate'].dt.day
df['PrescriptionGivenMonth'] = df['PrescriptionGivenDate'].dt.month
df['PrescriptionGivenYear'] = df['PrescriptionGivenDate'].dt.year
df['PrescriptiongivenDateIsWeekend'] = df['PrescriptionGivenDayOfWeek'].isin(['Saturday', 'Sunday'])
df['PrescriptiongivenDateIsHoliday'] = df['PrescriptionGivenDate'].isin(holidays)
df['PrescriptionGivenSeason'] = df['PrescriptionGivenMonth'].apply(determine_season)

df['PrescriptionExpirationDate'] = pd.to_datetime(df['PrescriptionExpirationDate'])
df['PrescriptionExpirationDayOfWeek'] = pd.to_datetime(df['PrescriptionExpirationDate']).dt.day_name()
df['PrescriptionExpirationDay'] = df['PrescriptionExpirationDate'].dt.day
df['PrescriptionExpirationMonth'] = df['PrescriptionExpirationDate'].dt.month
df['PrescriptionExpirationYear'] = df['PrescriptionExpirationDate'].dt.year
df['PrescriptionExpirationDateIsWeekend'] = df['PrescriptionExpirationDayOfWeek'].isin(['Saturday', 'Sunday'])
df['PrescriptionExpirationDateIsHoliday'] = df['PrescriptionExpirationDate'].isin(holidays)
df['PrescriptionExpirationSeason'] = df['PrescriptionExpirationMonth'].apply(determine_season)




# Calcul du profit
df['Profit'] = round(df['SellPrice'] - df['BuyPrice'],2)

# Sauvegarde dans un fichier CSV
df.to_csv('outputSQL.csv', index=False)

